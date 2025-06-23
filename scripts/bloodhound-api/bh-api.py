#!/usr/bin/python3
import requests
import json
import argparse

parser = argparse.ArgumentParser(description='BloodHound CE API calls')
parser.add_argument("--url", type=str, default='http://localhost:8080', help='')
parser.add_argument("-u", "--username", type=str, default='admin', help='')
parser.add_argument("-p", "--password", type=str, default='Bloodhound1!', help='')
parser.add_argument("-z", "--zip", type=str, help='Zip file for the upload')

parser.add_argument("-c", "--clear", action="store_true", help="Clear database")

parser.add_argument("-l", "--list", action="store_true", help='List all custom queries')
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
    session_token= r.json().get("data", {}).get("session_token")
    if session_token != None:
        print(f'\033[92m[+]\033[0m Logged in successfully\n')
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

def list_jobs():
    r = requests.get(f"{args.url}/api/v2/file-upload", headers=TOKEN)
    data = r.json()
    print(json.dumps(data, indent=2))

def start_job():
    r = requests.post(f"{args.url}/api/v2/file-upload/start", headers=TOKEN)
    data = r.json()
    print(json.dumps(data, indent=2))
    return data.get("data", {}).get("id")

def upload(file_upload_job_id):
    headers = {
        "Authorization": f"Bearer {session_token}",
        "Content-Type": "application/zip"
        }
    with open(args.zip, "rb") as f:
        files = {
            "file": ("upload.zip", f, "application/zip")
        }
    r = requests.post(f"{args.url}/api/v2/file-upload/{file_upload_job_id}", headers=headers, files=files)
    data = r.json()
    print(json.dumps(data, indent=2))

def clear_database():
    data = {
        "deleteCollectedGraphData": True,
        "deleteFileIngestHistory": True,
        "deleteDataQualityHistory": True,
        "deleteAssetGroupSelectors": [0]
    }
    r = requests.post(f"{args.url}/api/v2/clear-database", json=data, headers=TOKEN)
    print(f"[!] Database cleard - {r.status_code}")

session_token = login()
TOKEN = {"Authorization": f"Bearer {session_token}"}
if args.file:
    add_query_from_list()
if args.query:
    run_query(args.query)
if args.remove:
    if args.remove.lower() == 'all':
        remove_all_queries()
    else:
        remove_query(args.remove)

if args.list:
    list_queries()

if args.clear:
    clear_database()

if args.zip:
    upload(start_job())
    print("----")
    list_jobs()
