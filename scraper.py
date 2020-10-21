import pandas as pd
from urllib.request import FancyURLopener
from bs4 import BeautifulSoup
import requests
import re
import math
from tqdm import tqdm


def get_caldo(url):
    content = requests.get(url).content
    return BeautifulSoup(content, 'lxml')


def get_title(caldo):
    title = caldo.find('h1', class_='title mathjax')
    title.find('span').extract()
    return title.getText().strip()


def get_authors(caldo):
    authors = caldo.find('div', class_='authors')
    authors.find('span').extract()
    return authors.getText()


def get_subjects(caldo):
    subjects = caldo.find('td', class_='tablecell subjects')
    main_subj_aux = subjects.find('span')
    main_subj = main_subj_aux.getText().strip()
    main_subj_aux.extract()
    subjects = subjects.getText().strip()
    return (main_subj, subjects)


def get_abs(caldo):
    _abs = caldo.find('blockquote', class_='abstract mathjax')
    _abs.find('span').extract()
    return _abs.getText().strip()


def get_fecha(caldo):
    fecha = caldo.find('div', class_='dateline')
    return fecha.getText().strip()


if __name__ == '__main__':
    df_link = pd.read_csv('df_Joel.csv')
    links = df_link['link']
    titles = []
    authors = []
    main_subjs = []
    subjects = []
    abstracts = []
    dates = []
    counter = 0
    batch_size = 1000

    for url in tqdm(links):
        counter += 1

        if counter % batch_size == 0:
            df_data = pd.DataFrame()
            df_data = df_data.from_dict({"title": titles, "author": authors, "abstractstract": abstracts, "main_subject": main_subjs,
                                         "other_subjects": subjects, "submission_date": dates})

            df_data.to_csv('data_joel{}.csv'.format(counter), index=False)

            titles = []
            authors = []
            main_subjs = []
            subjects = []
            abstracts = []
            dates = []

        try:
            caldo_de_gallina = get_caldo(url)
            title = get_title(caldo_de_gallina)
            author = get_authors(caldo_de_gallina)
            main_s, subjs = get_subjects(caldo_de_gallina)
            date = get_fecha(caldo_de_gallina)
            _abs = get_abs(caldo_de_gallina)

            titles.append(title)
            authors.append(author)
            main_subjs.append(main_s)
            subjects.append(subjs)
            abstracts.append(_abs)
            dates.append(date)
        except:
            pass

    df_data = pd.DataFrame()
    df_data = df_data.from_dict({"title": titles, "author": authors, "abstract": abstracts, "main_subject": main_subjs,
                                 "other_subjects": subjects, "submission_date": dates})

    df_data.to_csv('data_joel{}.csv'.format(counter), index=False)
