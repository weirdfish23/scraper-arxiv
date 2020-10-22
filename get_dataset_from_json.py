import pandas as pd
import json
from tqdm import tqdm
import math


def get_data_from_json(json_string, fields):
    j_dict = json.loads(json_string)
    data_dict = {}
    for key in fields:
        data_dict[key] = j_dict[key]
    return data_dict


def get_dataset_from_json(file_name, fields, max_data, inicio, fin):
    df = pd.DataFrame(columns=fields)
    with open(file_name, 'r') as f:
        for i, line in tqdm(enumerate(f), total=max_data):
            if (i >= max_data):
                break

            if i >= inicio and i < fin:
                data = get_data_from_json(line, fields)

                # Solo guardar papers con main_subject de computer science
                if 'cs.' == data['categories'].strip()[:3]:
                    df = df.append(data, ignore_index=True)

    return df


if __name__ == "__main__":
    file_name = 'arxiv-metadata-oai-snapshot.json'
    fields = ['id', 'title', 'authors', 'abstract', 'categories',
              'versions', 'comments', 'journal-ref', 'doi', 'report-no']
    # Data available:
    # ['id', 'submitter', 'authors', 'title', 'comments', 'journal-ref', 'doi', 'report-no', 'categories', 'license', 'abstract', 'versions', 'update_date', 'authors_parsed']
    max_data = 1778380  # MAX 1778380
    start = 0
    step = 445000

    for i in range(math.ceil((max_data-start)/step)):
        df = get_dataset_from_json(
            file_name, fields, max_data=max_data, inicio=i*step+start, fin=i*step+start+step)

        # split categories
        df['main_subject'] = df['categories'].apply(lambda x: x.split()[0])
        df['other_subjects'] = df['categories'].apply(
            lambda x: ' '.join(x.split()[1:]))
        df = df.drop('categories', axis=1)

        df.to_csv(f'arxiv_dataset_{i}.csv', index=False)
        print('csv', i+1, '->', len(df), 'registros leidos')
