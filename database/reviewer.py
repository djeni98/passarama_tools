#!/usr/bin/python3
import os, sys
import argparse

def ignore_link():
    inp = None
    while inp is None:
        inp = input('Ignore this link? [y/N] ')
        no = ['', 'n', 'N', 'no', 'No', 'NO']
        yes = ['y', 'Y', 'yes', 'Yes', 'YES']

        if inp in yes:
            return True
        elif inp in no:
            return False

        print('[Use "yes" or "no"]', end = ' ')
        inp = None

def review_links(review_file, count=None):
    links_ignore = []
    review = []

    with open(review_file, 'r') as f:
        file_size = sum(1 for _ in f)

    with open(review_file, 'r') as f:
        if count:
            print(f'Reviewing {count} links')
        else:
            print(f'Reviewing {file_size} links')

        for idx, line in enumerate(f):
            if count is not None and count < idx + 1:
                review.append(line)
                continue

            link = line[:-1]
            print(f'({idx + 1}) Opening "{link}"')

            os.system(f'firefox {link}')

            if ignore_link():
                links_ignore.append(link)

    if len(review):
        print(f'There are {len(review)} links to be reviewed')
        with open(review_file, 'w') as f:
            for line in review:
                f.write(line)
    else:
        print(f'Removing "{review_file}"')
        os.system(f'rm {review_file}')

    with open('links-ignore.txt', 'a') as f:
        for link in links_ignore:
            f.write(link + '\n')

    return links_ignore
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Review new links extracted by crawler')
    parser.add_argument('-c', '--count', metavar='LINES',
                        default=None)
    parser.add_argument('-f', '--file', default='review-links.txt')

    arguments = vars(parser.parse_args())
    review_links(arguments['file'], arguments['count'])
