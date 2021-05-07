import json
import requests
import datetime

config_file = './Data/config.json'
refresh_file = './Data/refresh_token.json'
access_file = './Data/access_token.json'

def load_config(filename, key):
    with open(filename, 'r') as f:
        return json.load(f)[key]
        
def update_refresh_token(refresh_file, config_file):
    token = load_config(refresh_file, 'refresh_token')
    client_id = load_config(config_file, 'client_id')
    endpoint = load_config(config_file, 'endpoint_auth')

    parameters = {
        'grant_type': 'refresh_token',
        'refresh_token': token,
        'access_type': 'offline',
        'code': '',
        'client_id': client_id
    }
    response = requests.post(url=endpoint, data=parameters).json()
    response['expiration_time'] = (datetime.datetime.now()+datetime.timedelta(seconds=response['refresh_token_expires_in'])).strftime('%Y%m%d_%H:%M:%S')
    with open('./Data/refresh_token.json', 'w') as f:
        json.dump(response, f)

def update_access_token(refresh_file, config_file):
    token = load_config(refresh_file, 'refresh_token')
    client_id = load_config(config_file, 'client_id')
    endpoint = load_config(config_file, 'endpoint_auth')
    
    parameters = {
        'grant_type': r'refresh_token',
        'refresh_token': token,
        'access_type': '',
        'code': '',
        'client_id': client_id
    }
    response = requests.post(url=endpoint, data=parameters).json()
    response['expiration_time'] = (datetime.datetime.now()+datetime.timedelta(seconds=response['expires_in'])).strftime('%Y%m%d_%H:%M:%S')
    with open('./Data/access_token.json', 'w') as f:
        json.dump(response, f)

def update_token(refresh_file, access_file, config_file):
    refresh_expiration = load_config(refresh_file, 'expiration_time')
    access_expiration = load_config(access_file, 'expiration_time')
    refresh_expires = datetime.datetime.strptime(refresh_expiration, '%Y%m%d_%H:%M:%S')-datetime.datetime.now()
    access_expires = datetime.datetime.strptime(access_expiration, '%Y%m%d_%H:%M:%S')-datetime.datetime.now()
    
    if refresh_expires < datetime.timedelta(seconds=604800):
        update_refresh_token(refresh_file, config_file)
        print('Refresh token updated.')
    if access_expires < datetime.timedelta(seconds=360):   
        update_access_token(refresh_file, config_file)
        print('Access token updated.')
    else:
        print("Tokens are still active. Refresh expires in {}. Access expires in: {}".format(refresh_expires, access_expires))

def get_quote(refresh_file, access_file, config_file, symbol, save=0):
    update_token(refresh_file, access_file, config_file)
    access_token = load_config(access_file, key='access_token')
    endpoint = load_config(config_file, key='endpoint_quote')
    
    payload = {'Authorization': r'Bearer {}'.format(access_token)}
    
    parameters = {}
    
    response = requests.get(url=endpoint.format(symbol), headers=payload, params=parameters).json()
    if save:
        with open('./Data/{}_quote_{}.json'.format(symbol, datetime.datetime.today().strftime('%Y%m%d_%H%M%S')), 'w') as working_data:
            json.dump(response, working_data)
    return response
        
def get_chain(refresh_file, access_file, config_file, symbol, save=0):
    update_token(refresh_file, access_file, config_file)
    access_token = load_config(access_file, key='access_token')
    endpoint = load_config(config_file, key='endpoint_chain')
    
    payload = {'Authorization': r'Bearer {}'.format(access_token)}
    
    parameters = {
        "symbol": symbol
    }
    
    response = requests.get(url=endpoint.format(symbol), headers=payload, params=parameters).json()
    
    if save:
        with open('./Data/{}_chain_{}.json'.format(symbol, datetime.datetime.today().strftime('%Y%m%d_%H%M%S')), 'w') as working_data:
            json.dump(response, working_data)
    return response
        
        
        
if __name__ == "__main__":
    get_quote(refresh_file, access_file, config_file, "AMZN", save=1)
    get_chain(refresh_file, access_file, config_file, "AMZN", save=1)
        
        
