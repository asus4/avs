import json
import logging
import sys
import time

import requests
# from hyper import HTTPConnection

capabilities = {
    'envelopeVersion': '20160207',
    'capabilities': [
        {
            'type': 'AlexaInterface',
            'interface': 'Alerts',
            'version': '1.0'
        },
        # {
        #     'type': 'AlexaInterface',  
        #     'interface': 'AudioActivityTracker',
        #     'version': '1.0'
        # },
        {
            'type': 'AlexaInterface',
            'interface': 'AudioPlayer',
            'version': '1.0'
        },
        # {
        #     'type': 'AlexaInterface',
        #     'interface': 'Bluetooth',
        #     'version': '1.0'
        # },
        # {
        #     'type': 'AlexaInterface',
        #     'interface': 'EqaulizerController',
        #     'version': '1.0'
        # },
        # {
        #     'type': 'AlexaInterface',
        #     'interface': 'Alexa.InputController',
        #     'version': '1.0'
        # },
        # {
        #     'type': 'AlexaInterface',
        #     'interface': 'InteractionModel',
        #     'version': '1.0'
        # },
        {
            'type': 'AlexaInterface',
            'interface': 'Notifications',
            'version': '1.0'
        },
        {
            'type': 'AlexaInterface',
            'interface': 'PlaybackController',
            'version': '1.0'
        },
        {
            'type': 'AlexaInterface',
            'interface': 'Settings',
            'version': '1.0'
        },
        {
            'type': 'AlexaInterface',
            'interface': 'Speaker',
            'version': '1.0'
        },
        {
            'type': 'AlexaInterface',
            'interface': 'SpeechRecognizer',
            'version': '1.0'
        },
        {
            'type': 'AlexaInterface',
            'interface': 'SpeechSynthesizer',
            'version': '1.0'
        },
        {
            'type': 'AlexaInterface',
            'interface': 'System',
            'version': '1.0'
        },
        # {
        #     'type': 'AlexaInterface',
        #     'interface': 'TemplateRuntime',
        #     'version': '1.0'
        # },
        # {
        #     'type': 'AlexaInterface',
        #     'interface': 'VisualActivityTracker',
        #     'version': '1.0'
        # }
    ]
}

def send(config):
    '''
    Send config
    https://developer.amazon.com/docs/alexa-voice-service/capabilities-api.html
    '''
    
    logger = logging.getLogger(__name__)

    endpoint = 'https://api.amazonalexa.com/v1/devices/@self/capabilities'
    # endpoint = 'https://api.amazonalexa.com/v1/devices/{}/capabilities'.format(config['client_id'])
    
    # option: NO space 
    jsonStr = json.dumps(capabilities, separators=(',',':'))
    # data = bytes(jsonStr, 'utf-8')
    data = jsonStr.encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'Content-Length': str(len(data)),
        # 'x-amz-access-token': 'Bearer {}'.format(config['access_token']),
        'Authorization': 'Bearer {}'.format(config['access_token']),
        'Accept': '',
        'Expect': '',
    }
    # print data
    # print headers
    # print config
    logger.info('send request')
    logger.info('headers: %s', headers)
    logger.info('data: %s', data)

    res = requests.post(endpoint, json=data, headers=headers)
    logger.info(res)
    logger.warning(res.text)
    return res.status_code

def send_retries(config, retry_count):
    logger = logging.getLogger(__name__)

    code = send(config)
    logger.info(code)

    if code is 204:
        logger.info('Sucseed')
        return

    retry_count = retry_count + 1
    if retry_count > 3:
        logger.warn('giveup to retry')
        return
    
    wait_time = retry_count * retry_count 
    logger.info('Retry %d times wait for %s', retry_count, wait_time)
    time.sleep(wait_time)
    send_retries(config, retry_count)



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    import config
    send_retries(config.load(), 0)