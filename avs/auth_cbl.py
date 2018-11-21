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
    curl -k -d 'response_type=device_code&client_id={{client_id}}&scope=alexa%3Aall&scope_data=%7B%22alexa%3Aall%22%3A%7B%22productID%22%3A%22Speaker%22,%22productInstanceAttributes%22%3A%7B%22deviceSerialNumber%22%3A%2212345%22%7D%7D%7D' -H "Content-Type: application/x-www-form-urlencoded" -X POST https://api.amazon.com/auth/O2/create/codepair
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
    return r.json()


def auth(config, output):
    """
    Implements code based auth
    https://developer.amazon.com/docs/alexa-voice-service/code-based-linking-other-platforms.html
    """

    config = avs.config.load(config) if config else {}

    res = get_user_code(config)
    print(res)

@click.command()
@click.option('--config', '-c', help='configuration json file with product_id, client_id and client_secret')
@click.option('--output', '-o', default=avs.config.DEFAULT_CONFIG_FILE, help='output json file with refresh token')
def main(config, output):
    auth(config, output)


if __name__ == '__main__':
    main()