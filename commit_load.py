import requests
import os
import sys
import duckdb
import logging

GITHUB_TOKEN=os.getenv("GITHUB_TOKEN")
GITHUB_AUTH_HEADER={"Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else {}}
REPOS = [
    ('pandas-dev', 'pandas'),
    ('numpy', 'numpy'),
    ('plotly', 'plotly'),
    ('matplotlib', 'matplotlib'),
    ('scikit-learn', 'scikit-learn'),
]
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='commit_load.log')
logger=logging.getLogger(__name__)

def get_next_page(page):
    return page if page.headers.get('link')!=None else None

def get_commits(url):   #enter api python package url here
    session=requests.Session()
    params={'per_page':100}
    first_page=session.get(url, headers=GITHUB_AUTH_HEADER, params=params)
    yield first_page

    next_page=first_page
    while get_next_page(next_page) is not None:
        try:
            next_page_url=next_page.links['next']['url']
            next_page=session.get(next_page_url, headers=GITHUB_AUTH_HEADER, params=params)
            yield next_page
        except KeyError:
            print("No more pages to fetch.")
            break
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            break

def create_table():
    con.execute("""CREATE OR REPLACE TABLE commits (package VARCHAR, date TIMESTAMPTZ, author VARCHAR);""")
    logger.info("Created commits table in DuckDB database.")

def process_commits(package, commit):
    if commit['author']['name'] != 'dependabot[bot]':
        con.execute(f"""INSERT INTO commits VALUES (?,?, ?);""", (package,commit['author']['date'], commit['author']['name']))
        logger.info(f"Inserted commit data into commits table: {commit['author']['name']}")

if __name__ == "__main__":
    try:
        con=duckdb.connect(database='packages.duckdb',read_only=False)
        logger.info("Connected to DuckDB database.")
        create_table()

        for package in REPOS:
            for page in get_commits(f"https://api.github.com/repos/{package[0]}/{package[1]}/commits"):  
                commits=page.json()
                for c in commits:
                    process_commits(package[1],c['commit'])
        #             print(c['commit']['author']['name'],'\n')
        #             print(c['commit']['message'])

    except KeyboardInterrupt:
        quota_url="https://api.github.com/rate_limit"
        session=requests.Session()
        quota_response=session.get(quota_url, headers=GITHUB_AUTH_HEADER)
        quota_data=quota_response.json()
