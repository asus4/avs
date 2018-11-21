import datetime
import json
import os
import time
import uuid

import click
import requests

import avs.config


def get_user_code(config):
    """
    Step 2: in curl command
    """

    endpoint = 'https://api.amazon.com/auth/O2/create/codepair'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Language': config['locale'] if ('locale' in config) else 'en-US'
    }
    scope_data = json.dumps({
        'alexa:all': {
            'productID': config['product_id'],
            'productInstanceAttributes': {
                'deviceSerialNumber': uuid.uuid4().hex
            }
        }
    })
    payload = {
        'response_type': 'device_code',
        'client_id': config['client_id'],
        'scope': 'alexa:all',
        'scope_data': scope_data,
    }
    r = requests.post(endpoint, data=payload, headers=headers)
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()

def get_device_token(code_response):
    """
    Step 2: Request the device token 
    """

    endpoint = 'https://api.amazon.com/auth/O2/token'
    headers = {
        'Host': 'api.amazon.com',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'grant_type': 'device_code',
        'device_code': code_response['device_code'],
        'user_code': code_response['user_code']
    }
    r = requests.post(endpoint, data=payload, headers=headers)
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        print('status: {} {}'.format(r.status_code, r.text))
        return None

def auth(config, output):
    """
    Implements code based auth
    https://developer.amazon.com/docs/alexa-voice-service/code-based-linking-other-platforms.html
    """

    config = avs.config.load(config) if config else {}

    code_res = get_user_code(config)
    print(code_res)
    print('Open {} and type code \"{}\"'.format(code_res['verification_uri'], code_res['user_code']))

    while True:
        time.sleep(10)
        token_res = get_device_token(code_res)
        if token_res is not None:
            break

    # Succeed to login
    print(json.dumps(token_res, indent=4))

    config['access_token'] = token_res['access_token']
    config['refresh_token'] = token_res['refresh_token']

    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=token_res['expires_in'])
    config['expiry'] = expiry_time.strftime('%a %b %d %H:%M:%S %Y')

    avs.config.save(config, configfile=output)


@click.command()
@click.option('--config', '-c', help='configuration json file with product_id, client_id and client_secret')
@click.option('--output', '-o', default=avs.config.DEFAULT_CONFIG_FILE, help='output json file with refresh token')
def main(config, output):
    auth(config, output)


if __name__ == '__main__':
    main()