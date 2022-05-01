from sodapy import Socrata
import requests
from requests.auth import HTTPBasicAuth
import argparse
import sys
import os
import json

parser = argparse.ArgumentParser(description='Process data from NYC Open Parking and Camera Violations.')
parser.add_argument('--page_size', type=int, help='How many rows do you want to get per page?', required=True)
parser.add_argument('--num_pages', type=int, help='How many pages do you want to get in total?')
args = parser.parse_args(sys.argv[1:])

INDEX_NAME=os.environ["INDEX_NAME"]
DATASET_ID=os.environ["DATASET_ID"]
APP_TOKEN=os.environ["APP_TOKEN"]
ES_HOST=os.environ["ES_HOST"]
ES_USERNAME=os.environ["ES_USERNAME"]
ES_PASSWORD=os.environ["ES_PASSWORD"]

if __name__ == '__main__':
    # Columns to fetch and analyze from dataset:
    fields = "state, license_type, issue_date, violation, fine_amount, summons_number"

    try:
        # URL to create "index" (elasticsearch database/table)
        resp = requests.put(f"{ES_HOST}/{INDEX_NAME}", auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD),
            # These are the "columns" of this database/table
            json={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1
                },
                "mappings": {
                    "properties": {
                        "state": {"type": "keyword" },
                        "license_type": {"type": "keyword" },
                        "issue_date": {"type": "date", "format": "mm/dd/yyyy" },
                        "violation": {"type": "keyword"},
                        "fine_amount": {"type": "float" },
                        "summons_number": {"type": "text"}
                    }
                }
            }
        )
        resp.raise_for_status()
        #print(resp.json())
    except Exception as e:
        print("Index already exists! Skipping")

    client = Socrata("data.cityofnewyork.us", APP_TOKEN, timeout=10000)

    # Checks if num_pages is entered, if it is,
    # fetch that number of pages and the specified rows (page_size) per page
    if args.num_pages is not None:
        rows=[]

        for i in range(0, args.page_size*args.num_pages, args.page_size):
            rows.extend(client.get(DATASET_ID, limit=args.page_size, offset=i, select=fields))

    # If num_pages is not entered, just grab the number of specified rows (page_size)
    else:
        rows=client.get(DATASET_ID, limit=args.page_size, select=fields)


    es_rows = []
    for row in rows:
        try:
            es_row = {}
            es_row["state"] = row["state"]
            es_row["license_type"] = row["license_type"]
            es_row["summons_number"] = row["summons_number"]
            es_row["issue_date"] = row["issue_date"]
            es_row["violation"] = row["violation"]
            es_row["fine_amount"] = float(row["fine_amount"])

        except Exception as e:
            print (f"Error!: {e}, skipping row: {row}")
            continue

        es_rows.append(es_row)

    bulk_upload_data = ""
    for line in es_rows:
        #print(f'Handling row {line["summons_number"]}')
        action = '{"index": {"_index": "' + INDEX_NAME + '", "_type": "_doc", "_id": "' + line["summons_number"] + '"}}'
        data = json.dumps(line)
        bulk_upload_data += f"{action}\n"
        bulk_upload_data += f"{data}\n"

    resp = requests.post(f"{ES_HOST}/_bulk", data=bulk_upload_data, auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD), headers={"Content-Type": "application/x-ndjson"})
    resp.raise_for_status()


    print ('Finished uploading to OpenSearch!')
