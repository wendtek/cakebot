import requests
import datetime
from pprint import pprint, pformat
import logging
import sys
import json
from util.config import config
import util.event_parser

logger = logging.getLogger()
if config['environment'] == 'local':
    logging.basicConfig(stream=sys.stdout, level=config['log_level'])
else:
    logger.setLevel(config['log_level'])


def handler(data, context):
    try:
        logger.info(pformat(data))
        event_body = json.loads(data['body'])

        logger.info(pformat(event_body))
        if not (verify_token(event_body.get('token')) or config['environment'] == 'local'):
            sys.exit()

        if event_body.get('challenge'):
            logger.info('Responding to challenge with {}'.format(event_body.get('challenge')))
            return {'statusCode': 200, 'body': event_body.get('challenge')}
        if data['headers'].get('X-Slack-Retry-Reason') == 'http_timeout':
            logger.info('Exiting because "X-Slack-Retry-Reason" header was set to "http_timeout"')
            return {'statusCode': 200}

        response = util.event_parser.generate_response(data['body'])

        post_to_slack({'text': response})

        return {'statusCode': 200, 'headers': {'X-Slack-No-Retry': 1}}

    except Exception as e:
        logger.error(e)
        return {'statusCode': 500, 'body': 'Error in lambda proxy', 'headers': {'X-Slack-No-Retry': 1}}


def post_to_slack(body):
    if not body:
        body = {
            'text': 'Cakebot test message from app in {}'.format(config['environment'])
        }

    res = requests.post(config['slack_webhook_url'], data=json.dumps(body))

    logger.info('Slack post status code: {}'.format(res.status_code))


def verify_token(token):
    try:
        if config['slack_verification_token'] == token:
            logger.info('Slack token verified.')
            return True
        else:
            logger.info('Invalid Slack token provided.')
            return False
    except Exception:
        logger.info('No body.token in data object')
        return False


if __name__ == '__main__':
    handler(data={'body': '{}', 'headers': {}}, context=None)
