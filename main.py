from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pprint import pprint
import collections
import argparse
import datetime
import pandas

def get_years_caption(age_of_the_winery):
    if (age_of_the_winery%10==1) and (age_of_the_winery != 11) and (age_of_the_winery != 111):
        years_caption = "год"
    elif (age_of_the_winery%10>1) and (age_of_the_winery%10<5) and (age_of_the_winery!=12) and (age_of_the_winery!=13) and (age_of_the_winery!=14):
        years_caption = "года"
    else:
        years_caption = "лет"
    return years_caption

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Этот код нужен для более комфортного и просто ведения сайта по продаже вин.'
    )
    parser.add_argument('file_path', help='Путь к файлу')
    args = parser.parse_args()

    wines = pandas.read_excel(args.file_path, na_filter=False).to_dict(orient='record')
    menu = collections.defaultdict(list)
    for categories in wines:
      menu[categories['Категория']].append(categories)

    now_time = datetime.datetime.now()
    age_of_the_winery = now_time.year - 1920

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        years_caption=get_years_caption(age_of_the_winery),
        age_of_the_winery = age_of_the_winery,
        menu=menu
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
