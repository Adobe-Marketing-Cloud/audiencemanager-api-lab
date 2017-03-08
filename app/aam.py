
import requests, time, json
from django.conf import settings as configs


GET    = 'GET'
POST   = 'POST'
PUT    = 'PUT'
DELETE = 'DELETE'


# generic method that will exchange API requests between client and AAM
def api_exchange(method, url, payload=None):

    print ('AAM API Request: %s %s Payload:%s' % (method, url, str(payload)))

    headers = {
        'Authorization': 'Bearer ' + configs.AAM_API_ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    if method == GET:
        response = requests.get(url, headers=headers)
    elif method == POST:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
    elif method == PUT:
        response = requests.put(url, headers=headers, data=json.dumps(payload))
    elif method == DELETE:
        response = requests.delete(url, headers=headers)
    else:
        raise ValueError('Unsupported HTTP method: %s' % method)

    print ('AAM API Response: %s' % response.status_code)
    if response: print json.dumps(response.json(), indent=4)
    return response


# checks whether the response from the request was successful
def successful(response):
    return response is not None and response.status_code in [200, 201, 204]


def get_self():
    response = api_exchange(GET, configs.AAM_SELF_USER_API_PATH)
