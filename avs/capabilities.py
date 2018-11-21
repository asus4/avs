import json
import logging
import time
import requests

logger = logging.getLogger(__name__)

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

def send(token):
    '''
    Send config
    https://developer.amazon.com/docs/alexa-voice-service/capabilities-api.html
    '''
    
    logger = logging.getLogger(__name__)

    endpoint = 'https://api.amazonalexa.com/v1/devices/@self/capabilities'
    
    jsonStr = json.dumps(capabilities, separators=(',',':'))
    data = jsonStr.encode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'Content-Length': str(len(data)),
        'Authorization': 'Bearer {}'.format(token),
    }
    logger.debug('headers: %s', headers)
    logger.debug('data: %s', data)

    res = requests.put(endpoint, data=data, headers=headers)
    return res.status_code

def send_retries(token, retry_count = 0):

    code = send(token)
    if code is 204:
        logger.info('Sucseed setting capabilities')
        return

    retry_count = retry_count + 1
    if retry_count > 3:
        logger.warn('giveup to retry')
        return
    
    wait_time = retry_count * retry_count 
    logger.info('Got %d, Retrying %d times wait for %s',code, retry_count, wait_time)
    time.sleep(wait_time)
    send_retries(token, retry_count)



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    import config
    conf = config.load()
    send_retries(conf['access_token'], 0)