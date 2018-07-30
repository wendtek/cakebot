import os
import logging


def getLogLevel(level_string):
    case = {
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG,
        'notset': logging.NOTSET
    }
    return case.get(level_string.lower(), logging.INFO)


config = {}

config['fooda_account_id'] = os.environ['FOODA_ACCOUNT_ID']
config['fooda_building_id'] = os.environ['FOODA_BUILDING_ID']
config['fooda_seed_event_id'] = os.environ['FOODA_SEED_EVENT_ID']
config['slack_bot_oauth_token'] = os.environ['SLACK_BOT_OAUTH_TOKEN']
config['slack_verification_token'] = os.environ['SLACK_VERIFICATION_TOKEN']
config['slack_webhook_url'] = os.environ['SLACK_WEBHOOK_URL']
config['log_level'] = getLogLevel(os.environ['LOG_LEVEL'])
config['environment'] = os.environ['RUNTIME_ENVIRONMENT']
