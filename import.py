import requests
import json
import os
import time

headers = {
   'Accept-Language': 'en-US,en;q=0.9',
   'Connection': 'keep-alive',
   'Cookie': os.getenv('COOKIE'),
   'DNT': '1',
   'Origin': 'https://www.startupschool.org',
   'Referer': 'https://www.startupschool.org/cofounder-matching/',
   'Sec-Fetch-Dest': 'empty',
   'Sec-Fetch-Mode': 'cors',
   'Sec-Fetch-Site': 'same-origin',
   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
   'accept': '*/*',
   'content-type': 'application/json',
   'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"macOS"',
   'x-csrf-token': os.getenv('X_CSRF_TOKEN'),
}

json_data = {
    'operationName': 'COFOUNDER_MATCHING_CANDIDATE',
    'variables': {
        'slug': 'next',
    },
    'query': 'query COFOUNDER_MATCHING_CANDIDATE($slug: ID) {\n  cofounderMatching {\n    invitesRemaining\n    profile {\n      ...CFMViewerProfileFragment\n      slug\n      active\n      email\n      user {\n        slug\n        isWoman\n        country\n        region\n        admin\n        __typename\n      }\n      __typename\n    }\n    candidate(slug: $slug) {\n      ...CFMProfileFragment\n      id\n      userId\n      fymkAffinity\n      request {\n        slug\n        status\n        message\n        sender {\n          slug\n          user {\n            slug\n            name\n            country\n            region\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CFMProfileFragment on CofounderProfile {\n  ...BasicProfileFragment\n  canInviteTrial\n  conversationSlug\n  metAtSpeedDatingToday\n  fymkAffinity\n  company {\n    ...BasicCompanyFragment\n    __typename\n  }\n  user {\n    ...BasicCfmUserFragment\n    __typename\n  }\n  request {\n    slug\n    status\n    __typename\n  }\n  __typename\n}\n\nfragment BasicProfileFragment on CofounderProfile {\n  active\n  approvalStatus\n  timing\n  email\n  emailSettings\n  hasIdea\n  ideas\n  hasCf\n  currentCfLinkedin\n  currentCfTechnical\n  whyLookingForThirdCf\n  interests\n  intro\n  lastSeenAt\n  equity\n  freeTime\n  lifeStory\n  other\n  reqFreeText\n  responsibilities\n  slug\n  videoLink\n  calendlyLink\n  fymkAffinity\n  ...CofounderPreferenceFragment\n  __typename\n}\n\nfragment CofounderPreferenceFragment on CofounderProfile {\n  cfHasIdea\n  cfHasIdeaImportance\n  cfIsTechnical\n  cfIsTechnicalImportance\n  cfResponsibilities\n  cfResponsibilitiesImportance\n  cfLocation\n  cfLocationImportance\n  cfLocationKmRange\n  cfAgeMin\n  cfAgeMax\n  cfAgeImportance\n  cfTimingImportance\n  cfInterestsImportance\n  cfIsFellowAlumniImportance\n  cfIsWomanImportance\n  cfIsYcAlumImportance\n  __typename\n}\n\nfragment BasicCompanyFragment on PublicCompany {\n  description\n  name\n  progress\n  fundingStatus\n  slug\n  url\n  __typename\n}\n\nfragment BasicCfmUserFragment on User {\n  ...BasicUserFragment\n  firstName\n  country\n  region\n  __typename\n}\n\nfragment BasicUserFragment on User {\n  avatarUrl\n  impressiveThing\n  education\n  employment\n  isTechnical\n  isWoman\n  linkedin\n  location\n  name\n  slug\n  showYcFounder\n  schools {\n    ...SchoolFragment\n    __typename\n  }\n  ycFounderLabel\n  age\n  twitterLink\n  instagramLink\n  __typename\n}\n\nfragment SchoolFragment on School {\n  name\n  title\n  domain\n  colorPrimary\n  colorSecondary\n  __typename\n}\n\nfragment CFMViewerProfileFragment on CofounderProfile {\n  slug\n  email\n  intro\n  hasIdea\n  timing\n  responsibilities\n  interests\n  cfIsWomanImportance\n  cfIsYcAlumImportance\n  cfIsFellowAlumniImportance\n  ...CofounderPreferenceFragment\n  user {\n    ...BasicCfmUserFragment\n    __typename\n  }\n  __typename\n}\n',
}

def get_next():
    response = requests.post('https://www.startupschool.org/graphql', headers=headers, json=json_data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Request failed with status code', response.status_code)

if __name__ == "__main__":
   ids = set()
   result = []

   response_json = get_next()
   response_id = response_json["data"]["cofounderMatching"]["candidate"]["slug"]

   i = 0
   # Fetch up to 10000 candidates
   while response_id not in ids or i >= 10000:
      ids.add(response_id)
      result.append(response_json)

      # let's be nice
      time.sleep(200/1000) # 200 ms

      i += 1
      response_json = get_next()
      response_id = response_json["data"]["cofounderMatching"]["candidate"]["slug"]
    
   # Write the results to a file
   with open('response_data.json', 'w') as file:
      json.dump(result, file)
