# -*- coding: utf-8 -*-

"""https://developer.amazon.com/public/solutions/alexa/alexa-voice-service/reference/settings"""

import uuid

class Settings(object):
    
    def __init__(self, alexa):
        self.alexa = alexa

    @property
    def context(self):
        return {
            "header": {
                "namespace": "Settings",
                "name": "SettingsUpdated",
                "messageId": uuid.uuid4().hex
            },
            "payload": {
                "settings": [
                    {
                        "key": "locale",
                        "value": "ja-JP"
                    }
                ]
            }
        }
