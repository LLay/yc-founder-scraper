import json
import webbrowser
import argparse
from typing import List

def dict_to_object(d):
    # Convert the dictionary to an object
    obj = type('obj', (object,), d)
    # Recursively convert nested dictionaries to objects
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = dict_to_object(value)
    return obj

def energy_climate(single_response):
    candidate = single_response["data"]["cofounderMatching"]["candidate"]
    return \
        "energy" in candidate["interests"] and \
        "energy" in candidate["intro"] or "climate" in candidate["intro"]

queries = {
    "all": lambda _: True,
    "energy_climate": energy_climate,
}

def extract_urls(response_list: List[dict]) -> List[str]:
    return list(map(
        lambda x: f'https://www.startupschool.org/cofounder-matching/candidate/{x["data"]["cofounderMatching"]["candidate"]["slug"]}', 
        response_list
    ))

def main(data: List[object], query_name, max_urls):
    # filter the data with the given query
    query_results = list(filter(
        queries[query_name], 
        data
    ))

    # Open the resulting candidate urls in Chrome
    for url in extract_urls(query_results)[:max_urls]:
        webbrowser.get('chrome').open_new_tab(url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-q', '--query', type=str, help='The name of the query to run on the given data', required=True, choices=queries.keys())
    parser.add_argument('-m', '--max_urls', type=str, help='The maximum number of urls to open in the browser. Default:10', default=10)
    args = parser.parse_args()

    # Read the file containing the candidate profiles into memory
    with open('response_data.json', 'r') as file:
        # data = [dict_to_object(candidate) for candidate in json.load(file)]
        data = json.load(file)
        
        # Query the data and open the resulting profiles in chrome
        main(data, args.query, args.max_urls)
