import requests
import time
import json
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
    print 'AAM API user info:', json.dumps(response.json(), indent=4)


def get_or_create_shop_datasource():
    response = api_exchange(GET, configs.AAM_DATASOURCE_API_PATH + '?integrationCode=shop')

    found = False
    if successful(response) and len(response.json()) > 0:
        found = True
        datasource = response.json()[0]

    if not found:
        datasource = {
            'name': 'Shop Data Source',
            'integrationCode': 'shop',
            'uniqueTraitIntegrationCodes': True,
            'uniqueSegmentIntegrationCodes': True
        }
        response = api_exchange(POST, configs.AAM_DATASOURCE_API_PATH, datasource)
        datasource = response.json()
    print 'AAM datasource:', datasource
    return datasource


def get_category_trait_folder(category):
    folder_name = category.name
    trait_folder = None
    response = api_exchange(GET, configs.AAM_TRAIT_FOLDER_API_PATH)
    if successful(response):
        root_folder = response.json()[0]
        for sub_folder in root_folder['subFolders']:
            if sub_folder['name'] == folder_name:
                trait_folder = sub_folder
                break
    return trait_folder


def create_category_trait_folder(category):
    folder = {
        'name': category.name,
        'parentFolderId': 0
    }
    response = api_exchange(POST, configs.AAM_TRAIT_FOLDER_API_PATH, folder)
    print 'AAM trait folder create:', response
    return folder


def update_category_trait_folder(old_category, new_category):
    folder = get_category_trait_folder(old_category)
    if folder is not None:
        folder['name'] = new_category.name
        response = api_exchange(PUT, configs.AAM_TRAIT_FOLDER_API_PATH + '/' + str(folder['folderId']), folder)
        print 'AAM trait folder update:', response
        return folder
    else:
        return create_category_trait_folder(new_category)


def get_or_create_category_trait_folder(category):
    folder = get_category_trait_folder(category)
    if folder is not None:
        return folder
    else:
        return create_category_trait_folder(category)


def get_product_trait(product):
    trait_ic = 'product-' + str(product.id)
    response = api_exchange(GET, configs.AAM_TRAIT_API_PATH + '/ic:' + trait_ic)
    if successful(response):
        trait = response.json()
        return trait
    else:
        return None


def create_product_trait(product):
    trait_ic = 'product-' + str(product.id)
    trait = {
        'name': 'Interested in ' + product.name,
        'traitRule': 'product==' + str(product.id),
        'folderId': get_or_create_category_trait_folder(product.category)['folderId'],
        'dataSourceId': get_or_create_shop_datasource()['dataSourceId'],
        'integrationCode': trait_ic,
        'traitType': 'RULE_BASED_TRAIT'
    }
    response = api_exchange(POST, configs.AAM_TRAIT_API_PATH, trait)
    trait = response.json()
    print 'AAM trait create:', trait
    return trait


def update_product_trait(old_product, new_product):
    trait = get_product_trait(old_product)
    if trait is not None:
        trait['name'] = 'Interested in ' + new_product.name
        response = api_exchange(PUT, configs.AAM_TRAIT_API_PATH + '/' + str(trait['sid']), trait)
        trait = response.json()
        print 'AAM trait update:', trait
        return trait
    else:
        return create_product_trait(new_product)


def get_or_create_product_trait(product):
    trait = get_product_trait(product)
    if trait is not None:
        return trait
    else:
        return create_product_trait(product)


def get_category_segment(category):
    segment_ic = 'category-' + str(category.id)
    response = api_exchange(GET, configs.AAM_SEGMENT_API_PATH + '/ic:' + segment_ic)
    if successful(response):
        segment = response.json()
        return segment
    else:
        return None


def generate_segment_rule_for_category(category):
    trait_sids = []
    for product in category.get_products():
        trait_sids.append(str(get_or_create_product_trait(product)['sid']) + 'T')
    print trait_sids
    return ' OR '.join(trait_sids)

        
def create_category_segment(category):
    if len(category.get_products()) == 0:
        # no need to create segment because category has no products
        return

    segment_ic = 'category-' + str(category.id)
    segment_rule = generate_segment_rule_for_category(category)

    segment = {
        'name': 'Interested in ' + category.name,
        'segmentRule': segment_rule,
        'folderId': 0,
        'dataSourceId': get_or_create_shop_datasource()['dataSourceId'],
        'integrationCode': segment_ic
    }
    response = api_exchange(POST, configs.AAM_SEGMENT_API_PATH, segment)
    segment = response.json()
    print 'AAM segment create:', segment
    map_segment_to_destination(segment['sid'])
    return segment


def update_category_segment(old_category, new_category):
    segment = get_category_segment(old_category)
    if segment is not None:
        segment['name'] = 'Interested in ' + new_category.name
        segment['segmentRule'] = generate_segment_rule_for_category(new_category)
        response = api_exchange(PUT, configs.AAM_SEGMENT_API_PATH + '/' + str(segment['sid']), segment)
        segment = response.json()
        print 'AAM segment update:', segment
    else:
        segment = create_category_segment(new_category)
    map_segment_to_destination(segment['sid'])
    return segment


def map_segment_to_destination(segment_id):
    destinationId = configs.AAM_DESTINATION_ID

    response = api_exchange(GET, configs.AAM_DESTINATION_API_PATH+ '/' + destinationId + '/mappings')
    if successful(response):
        mappings = response.json()
        for mapping in mappings:
            if mapping['sid'] == segment_id:
                return mapping

    mapping = {
        "traitType": "SEGMENT",
        "sid": segment_id,
        "startDate": "2017-02-14",
        "traitAlias": str(segment_id)
    }
    response = api_exchange(POST, configs.AAM_DESTINATION_API_PATH+ '/' + destinationId + '/mappings', mapping)
    mapping = response.json()

    print 'AAM segment mapping create:', mapping
    return mapping

