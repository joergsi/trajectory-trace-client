import requests
import json

# For access to non public sources you can generate the Basic Auth Header with 
# Username and Password here https://www.debugbear.com/basic-auth-header-generator
# For acces to public sources, just leave it as it is
# basic_auth = "Basic yourBase64encodedusernameandpassword"       # use this invalid basic_auth, for accessing public locations -> valid but not authorized ones throws always 502
# basic_auth = "Basic YWRtaW5AYWRtaW4ubG9jYWw6dGVzdDEyMw=="       # for local
basic_auth = "Basic am9lcmcuc2ljaGVybWFubkBlZnMtdGVjaGh1Yi5jb206QzVaS1hYVzkkbXNWVDc2OTJwRXpTVCZmUUZEXnghVjM="

# GraphiQL url
url = "https://city.app.sdk-cloud.de/api/graphql"
# url = "http://localhost:8080/api/graphql"

# Query
body = """
query Sensors {
  sensors(source: 1) {
    pageDuration
    totalCount
    nodes {
      id
      time
      class {
        name
      }
      knownAs
    }
  }
}
"""

# Request
response = requests.post(
    url=url, 
    json={"query": body}, 
    headers={"Authorization": basic_auth})
print("response status code: ", response.status_code)

# Print response
if response.status_code == 200:
    data = json.loads(response.content)
    print(json.dumps(data, indent = 4))

    # with open('query.json', 'w') as f:
    #     json.dump(data, f, indent=4)