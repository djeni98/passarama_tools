#!/usr/bin/python3
import sqlite3
import os, sys
import argparse

NEW_DB = 'test-dev.sqlite'
OLD_DB = 'old.sqlite'

def get_links_ignore(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute('SELECT link FROM linksIgnore')
    result = c.fetchall()

    conn.close()
    return [ item[0] for item in result ]


def get_dorama_links(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute('SELECT link FROM dorama')
    result = c.fetchall()

    conn.close()
    return [ item[0] for item in result ]

    
def insert_links_ignore(links, database, create=False):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    if create:
        c.execute('DROP TABLE IF EXISTS linksIgnore')
        c.execute(f'''
            CREATE TABLE linksIgnore (
                link TEXT NOT NULL PRIMARY KEY
            )
        ''')        
        conn.commit() 

    c.execute(f'''
        INSERT INTO linksIgnore
        VALUES {', '.join(['(?)' for l in links])}
        ''', [ l for l in links ]
    )
    conn.commit()
    conn.close()

def insert_old_doramas(links, database, create=False):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    if create:
        c.execute('DROP TABLE IF EXISTS oldDorama')
        c.execute(f'''
            CREATE TABLE oldDorama (
                link TEXT PRIMARY KEY
            )
        ''')        
        conn.commit() 

    c.execute(f'''
        INSERT INTO oldDorama
        VALUES {', '.join(['(?)' for l in links])}
        ''', [ l for l in links ]
    )
    conn.commit()
    conn.close()

def drop_dorama_links_ignore(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute(f'''
        DELETE FROM dorama
        WHERE dorama.link IN (
            SELECT link FROM linksIgnore
        )
    ''')
    
    conn.commit() 
    conn.close()

def get_new_links(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute(f'''
        SELECT d.link FROM dorama d
        LEFT JOIN linksIgnore l ON d.link = l.link
        LEFT JOIN oldDorama o ON d.link = o.link
        WHERE l.link IS NULL AND o.link IS NULL
    ''')
    
    result = c.fetchall()
    conn.close()
    return [ item[0] for item in result ]

 
def drop_old_dorama_table(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS oldDorama')
    conn.commit() 
    conn.close()


def initial_run():
    """
        Create linksIgnore table to save links to be ignored and
        drop these links from dorama table.

        Create oldDoramas table to save links from OLD_DB and
        get unreviewed links from difference between OLD_DB and NEW_DB dorama table
    """
        
    links_ignore = get_links_ignore(OLD_DB)
    dorama_links = get_dorama_links(OLD_DB)

    insert_links_ignore(links_ignore, NEW_DB, True)
    drop_dorama_links_ignore(NEW_DB)  # Drop already reviewed links

    insert_old_doramas(dorama_links, NEW_DB, True)
    review_links = get_new_links(NEW_DB)

    if not review_links:
        print('There\'s no links to be reviewed')
        return

    with open('review-links.txt', 'w') as f:
        for link in review_links:
            f.write(link + '\n')

    print('There are {} new link(s) to be reviewed'.format(len(review_links)))
    print('These links are stored at review-links.txt')


def final_run(filename, jump_links=False):
    """
        Get links to be ignored from file and drop them from dorama table

        Update old.sqlite with NEW_DB
    """
    links_ignore = []
    if not jump_links:
        with open(filename, 'r') as f:
            for line in f:
                links_ignore.append(line[:-1])

    if not links_ignore:
        print('There\'s no links to be removed')
    else:
        insert_links_ignore(links_ignore, NEW_DB, False)
        drop_dorama_links_ignore(NEW_DB)
        print('{} link(s) were removed'.format(len(links_ignore)))

    drop_old_dorama_table(NEW_DB)
    os.system(f'cp {NEW_DB} old.sqlite')


if __name__ == '__main__':
    help_initial = (
        'Compare OLD_DB with NEW_DB to get unreviewed links'
        '. It Generates "review-links.txt" file'
    )
    help_final = (
        'Drop ignored links and update old.sqlite with NEW_DB'
    )
    help_links = (
        'File to --final'
        '. Default "links-ignore.txt"'
    )

    parser = argparse.ArgumentParser(description='Clean dorama table in database. Use -i or -f.')
    parser.add_argument('-i', '--initial', action='store_true', help=help_initial)
    parser.add_argument('-f', '--final', action='store_true', help=help_final)
    parser.add_argument('-l', '--links', metavar='IGNORE_LINKS',
                        default='links-ignore.txt', help=help_links)
    parser.add_argument('-j', '--jump-links', action='store_true',
                        help='Skips dropping links step from --final')

    arguments = vars(parser.parse_args())

    if arguments['initial'] and not arguments['final']:
        print("Running initial...")
        initial_run()
    elif arguments['final'] and not arguments['initial']:
        print("Running final...")
        final_run(arguments['links'], arguments['jump_links'])
    else:
        parser.print_help()
        sys.exit(2)
