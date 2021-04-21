from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pprint import pprint
import datetime
import pandas


menu = {
    Белые Вина: ""
    Красные Вина: ""
}

excel_data_df = pandas.read_excel('wine2.xlsx', na_filter=False)

wines = excel_data_df.to_dict(orient='record')

pprint(menu)

now = datetime.datetime.now()

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    delta_years = now.year - 1920,
    menu=menu
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
