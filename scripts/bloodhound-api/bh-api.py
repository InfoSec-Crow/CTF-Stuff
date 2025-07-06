#!/usr/bin/python3
import requests
import json
import argparse
from time import sleep

parser = argparse.ArgumentParser(description='BloodHound CE edition API calls')
parser.add_argument("--url", type=str, default='http://localhost:8080', help='')
parser.add_argument("-u", "--username", type=str, default='admin', help='')
parser.add_argument("-p", "--password", type=str, default='Bloodhound1!', help='')

parser.add_argument("-z", "--zip", type=str, help='Zip file for the upload')
parser.add_argument("-c", "--clear", action="store_true", help="Clear database")
parser.add_argument("-lj", "--listjobs", action="store_true", help='List all jobs queries')

parser.add_argument("-lq", "--listquery", action="store_true", help='List all custom queries')
parser.add_argument("-f", "--file", type=str, help='Add custom queries from JSON file')
parser.add_argument("-r", "--remove", type=str, help='Remove a query, [id or "all"]')
parser.add_argument("-q", "--query", type=str, help='Query to run')

parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

args = parser.parse_args()

def login():
    print('[*] Login')
    login_data = {
        "login_method": "secret",
        "username": args.username,
        "secret": args.password
    }
    r = requests.post(f"{args.url}/api/v2/login", json=login_data)
    session_token = r.json().get("data", {}).get("session_token")
    if session_token != None:
        print(f'\033[92m[+]\033[0m Logged in successfully')
        if args.verbose:
            print(session_token)
        print()
    else:
        print(f'\033[91m[-]\033[0m Login falied')
        exit()
    return session_token

def list_queries(show=True):
    r = requests.get(f"{args.url}/api/v2/saved-queries", headers=TOKEN)
    data = json.loads(r.text)
    if show:
        print('[*] List queries')
        print(json.dumps(data, indent=2))
    return data
    
def add_query(name, query, description=''):
    print(f'[*] Add queries\n- Name: {name}\n- Query: {query}\n')
    data = {
        "name": name,
        "query": query,
        "description": description
    }
    r = requests.post(f"{args.url}/api/v2/saved-queries", json=data, headers=TOKEN)
    data = r.json()
    if "errors" in data and data["errors"]:
        message = data["errors"][0]["message"]
        print(f'\033[91m[-]\033[0m Error: {message}')
    else:
        print("\033[92m[+]\033[0m Query added successfully")
    if args.verbose:
        print(json.dumps(data, indent=2))
    print()

def add_query_from_list():
    with open(args.file, 'r') as f:
        data = json.load(f)
    for entry in data:
        add_query(entry.get('name'),entry.get('query'))

def run_query(query):
    data = {
    "query": query,
    "include_properties": True
    }
    r = requests.post(f"{args.url}/api/v2/graphs/cypher", json=data, headers=TOKEN)
    data = r.json()
    print(json.dumps(data, indent=2))

def remove_query(query_id):
    r = requests.delete(f"{args.url}/api/v2/saved-queries/{query_id}", headers=TOKEN)
    if r.status_code == 204:
        print(f"\033[92m[+]\033[0m Query ID: {query_id} removed successfully")
    else:
        print(f'\033[91m[-]\033[0m Remove query ID: {query_id} failed')

def remove_all_queries():
    for entry in list_queries(False).get('data'):
        remove_query(str(entry.get('id')))

def list_jobs(show=True):
    r = requests.get(f"{args.url}/api/v2/file-upload", headers=TOKEN)
    data = r.json()
    if show:
        print(json.dumps(data, indent=2))
    return data

def upload_zip(run=1, ids=[]):
    print("[*] Starting job")
    r = requests.post(f"{args.url}/api/v2/file-upload/start", headers=TOKEN)
    if r.status_code == 201:
        print("\033[92m[+]\033[0m Starting job successfully")
        r_content = r.content.decode('utf-8')
        json_obj = json.loads(r_content)
        file_upload_job_id = str(json_obj['data']['id'])
    else:
        print(f"\033[91m[-]\033[0m Starting job failed - {r.status_code}")
        exit()

    print(f"[*] Upload data to job {file_upload_job_id}")
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {session_token}',
        'Content-Type': 'application/zip',
    }
    with open(args.zip, mode='rb') as f:
        data = f.read()
    r = requests.post(f"{args.url}/api/v2/file-upload/{file_upload_job_id}", headers=headers, data=data)
    if r.status_code == 202:
        print("\033[92m[+]\033[0m Upload data successfully")
        print("[!] Wait 10 seconds for the file upload...")
        sleep(10)
    else:
        print(f"\033[91m[-]\033[0m Upload data failed - {r.status_code}")
        exit()

    print("[*] Ending job")
    r = requests.post(f"{args.url}/api/v2/file-upload/{file_upload_job_id}/end", headers=TOKEN)
    if r.status_code == 200:
        print("\033[92m[+]\033[0m Ending job successfully")
    else:
        print(f"\033[91m[-]\033[0m Ending job failed - {r.status_code}")
        exit()
    print("[*] Checking job status")
    check = True
    while check:
        r = list_jobs(False)
        for item in r["data"]:
            if item['id'] not in ids:
                status = "?"
                if item['status'] == 3:
                    status = "\033[91mCanceled\033[0m"
                    print(' ' * 80, end='\r')
                    print(f"[?] ID: {item['id']}, Status: {status}, Total Files: {item['total_files']}\n")
                    ids.append(item['id'])
                    upload_zip(run+1, ids)
                elif item['status'] == 6:
                    status = "\033[93mIngesting\033[0m"
                elif item['status'] == 2:
                    status = "\033[92mComplete\033[0m"
                    if item['total_files'] == 0:
                        status = "\033[91mCanceled\033[0m"
                        print(' ' * 80, end='\r')
                        print(f"[?] ID: {item['id']}, Status: {status}, Total Files: {item['total_files']}\n")
                        ids.append(item['id'])
                        upload_zip(run+1, ids)
                    print(' ' * 80, end='\r')
                    print(f"[?] ID: {item['id']}, Status: {status}, Total Files: {item['total_files']}\n")
                    exit()
                print(f"[?] ID: {item['id']}, Status: {status}, Total Files: {item['total_files']}", end='\r')
                sleep(2)

def clear_database():
    data = {
        "deleteCollectedGraphData": True,
        "deleteFileIngestHistory": True,
        "deleteDataQualityHistory": True,
        "deleteAssetGroupSelectors": [0]
    }
    r = requests.post(f"{args.url}/api/v2/clear-database", json=data, headers=TOKEN)
    if r.status_code == 204:
        print("\033[92m[+]\033[0m Database cleared successfully")
    else:
        print("\033[91m[-]\033[0m Database clearing failed")

session_token = login()
TOKEN = {
    "Authorization": f"Bearer {session_token}",
    "Accept": "application/json, text/plain, */*"
    }
if args.file:
    add_query_from_list()
if args.query:
    run_query(args.query)
if args.remove:
    if args.remove.lower() == 'all':
        remove_all_queries()
    else:
        remove_query(args.remove)
if args.listquery:
    list_queries()
if args.clear:
    clear_database()
if args.zip:
    upload_zip()
if args.listjobs:
    list_jobs()
