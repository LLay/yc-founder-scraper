# YCombinator candidate profile scraper

## Setup
``` bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Running it

### Download all your candidates

1. Log in to your YC cofounder account
2. Load a profile and extract the following info from the `graphql` request 
    - Session cookie
    - XSRF token
3. `touch .env`
4. Add the above auth data to this env file
5. `source .env`
6. `python import.py`

This will create a file called `response_data.json` containing all your matches.

### Search candidates; Open profiles in chrome.
Example:
```bash
python search.py --query all --max_urls 20
```

You'll want to write your own queries in `search.py` and execute them: 
```bash
python search.py --query my_named_query --max_urls 20
```

#### Usage
```bash
(env) Lyons-MacBook-Pro:yc-founder-scraper lyon$ python search.py -h
usage: search.py [-h] -q {all,energy_climate} [-m MAX_URLS]

arguments:
  -h, --help            show this help message and exit
  -q {all,energy_climate}, --query {all,energy_climate}
                        The name of the query to run on the given data
  -m MAX_URLS, --max_urls MAX_URLS
                        The maximum number of urls to open in the browser. Default:10
```
