#!/usr/bin/python3
import requests
import argparse

template = '''Olá moderadores,

Atualmente está sendo desenvolvido um projeto para facilitar
buscas de doramas e correlatos. O objetivo do projeto é
agilizar o processo de busca, ajudando a localizar em qual
fansub um dorama possa estar.

Por isso, venho notificá-los que seus links podem ser exibidos
nas buscas. Enfatizo o fato de que o link será do tópico e não
do(s) conteúdo(s) em si. Ao buscar uma palavra-chave, os dados
do resultado teriam as informações do título do dorama, o link
para o projeto na fansub e qual a fansub responsável.

Por exemplo, ao buscar "{KEYWORD}", seriam retornados os
seguintes resultados para a sua fansub.

{OBTAINED_RESULTS}

Como não há nenhuma restrição no termo de concordância para
compartilhar os links da fansub (novamente, não são os links
diretos), os dados já estão disponíveis no projeto.

O projeto possui algumas fansubs cadastradas em processo de
notificação. É possível visualizar os dados já existentes em:

{PASSARAMA}

Atenciosamente,
Projeto Passarama'''

PASSARAMA='https://passarama.netlify.app'
API='https://djeni.pythonanywhere.com'

def search_keyword_in_api(api, fansub, keyword):
    print(f'Searching "{keyword}" in fansub "{fansub}"...')
    r = requests.get('{}/doramas?fansub={}&title={}'.format(api, fansub, keyword))

    results = []
    for item in r.json().get('results', []):
        results += [f"* {item.get('title')}\n  fansub: {item.get('fansub')}\n  link: {item.get('link')}"]

    return '\n\n'.join(results)

def generate_text(fansub, keyword, site=PASSARAMA, api=API, template=template):
    results = search_keyword_in_api(api, fansub, keyword)
    return template.format(
        KEYWORD=keyword,
        OBTAINED_RESULTS=results,
        PASSARAMA=site
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create texts to notify data usage from a fansub'
    )
    parser.add_argument('-f', '--fansub', help='Fansub name', required=True)
    parser.add_argument('-k', '--keyword', help='Keyword to search for', required=True)
    parser.add_argument('-s', '--site', help='Passarama site - default: ' + PASSARAMA,
                        default=PASSARAMA)
    parser.add_argument('-a', '--api', help='Passarama api - default: ' + API,
                        default=API)
    parser.add_argument('-o', '--output', help='Output file')

    args = vars(parser.parse_args())

    text = generate_text(
        args['fansub'],
        args['keyword'],
        site=args['site'],
        api=args['api'],
        template=template
    )

    print('The message text has been generated.')

    if args['output']:
        with open(args['output'], 'w') as f:
            f.write(text)
        print(f'"{args["output"]}" file created.')
    else:
        print('-----------------------------------')
        print(text)


