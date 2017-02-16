import requests
import json


API_BASE_URL = 'https://api-beta.demdex.com/v1'


def exchange(method, url, payload=None, access_token=''):
    print ('AAM API call - %s %s payload:%s' % (method, url, str(payload)))
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, data=json.dumps(payload))
    elif method == 'PUT':
        response = requests.put(url, headers=headers, data=json.dumps(payload))
    elif method == 'DELETE':
        response = requests.delete(url, headers=headers)
    else:
        raise ValueError('Unsupported HTTP method: %s' % method)
    print ('AAM Response: %s' % response.status_code)
    return response


def get(url):
    global token
    return exchange('GET', API_BASE_URL + url, None, token)


def post(url, payload):
    global token
    return exchange('POST', API_BASE_URL + url, payload, token)


if __name__ == "__main__":
    global token
    token = raw_input('Enter token: ')
    partner_name = raw_input('Enter partner name: ')
    partner_subdomain = raw_input('Enter partner subdomain: ')
    user_username = raw_input('Enter username: ')
    user_password = raw_input('Enter password: ')

    partner = {
        'name': partner_name,
        'description': partner_name,
        'subdomain': partner_subdomain,
        'accountTypes': ['FULL_AAM', 'DATA_PROVIDER', 'VISITOR_ID_SERVICE'],
        'lifecycle': 'ACTIVE',   
    }
    response = post('/admin/partners/', partner)
    partner = response.json()
    print partner

    pid = partner['pid']
    user = {
        'pid': pid,
        'username': user_username,
        'firstName': user_username,
        'lastName': user_username,
        'email': user_username + '@adobe.com',
        'password': user_password,
        'admin': True
    }
    response = post('/users/', user)
    user = response.json()
    print user

    
    
    