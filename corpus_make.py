import json
import requests
import sys

def fetch_data(**params):
    url ='https://api.gnavi.co.jp/PhotoSearchAPI/v3/'
    response = requests.get(url, params = params)
    return response.json()

def extract_data(response):
    for key in response['response'].keys():
        if  not key.isdigit():
            continue
        d = response['response'][key]['photo']
        if d.get('comment') and d.get('total_score'):
            comment = d['comment']
            score = d['total_score']
            data = {
                'comment':comment,
                'score':score
            }
            yield data
def save_as_json(save_file, record):
    with open(save_file, mode = 'a') as f:
        f.write(json.dumps(record) + '\n')

def main():
    # 定数の設定
    raw_data = 'data/raw_data.json'
    save_file = 'data/dataset.json'
    keyid = '2202a3953472d44970dd4dbd86dc3fbf'
    # パラメータ
    response = fetch_data(
            keyid = keyid,
            area = '新宿',
            hit_per_page = 50,
            offset_page =1,
            )
    save_as_json(raw_data,response)
    records = extract_data(response)
    for record in records:
        save_as_json(save_file, record)
if __name__ == '__main__':
    main()
