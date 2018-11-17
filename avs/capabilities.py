import json
import logging

import requests


def send(config):
    '''
    Send config
    https://developer.amazon.com/docs/alexa-voice-service/capabilities-api.html
    '''
    
    logger = logging.getLogger(__name__)

    endpoint = 'https://api.amazonalexa.com/v1/devices/@self/capabilities'
    
    data = json.dumps({
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
    }).encode('utf-8')
    contentLength = len(data)
    headers = {
        'Content-Type': 'application/json',
        'Content-Length': bytes(contentLength),
        'Authorization': 'Bearer {}'.format(config['access_token'])
    }
    # print data
    # print headers
    # print config
    logger.info('send request')
    logger.info('headers: %s', headers)
    logger.info('data: %s', data)

    res = requests.post(endpoint, None, data, headers=headers)
    logger.info(res)
    logger.warning(res.text)

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    import config
    send(config.load())