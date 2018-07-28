from bs4 import BeautifulSoup
import requests
import datetime
import os
from urllib.parse import quote
from pprint import pprint, pformat
from decimal import Decimal
import logging
import sys
import json


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


fooda_account_id = os.environ['FOODA_ACCOUNT_ID']
fooda_building_id = os.environ['FOODA_BUILDING_ID']
fooda_seed_event_id = os.environ['FOODA_SEED_EVENT_ID']
slack_bot_oauth_token = os.environ['SLACK_BOT_OAUTH_TOKEN']
slack_verification_token = os.environ['SLACK_VERIFICATION_TOKEN']
slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
log_level = getLogLevel(os.environ['LOG_LEVEL'])
environment = os.environ['RUNTIME_ENVIRONMENT']

logger = logging.getLogger()
if environment == 'local':
    logging.basicConfig(stream=sys.stdout, level=log_level)
else:
    logger.setLevel(log_level)

slack_url = 'https://slack.com/api/chat.postMessage'
cookies = {}
cookies['context'] = quote(
    '{{"entity":"select_event","id":"{0}"}}'.format(fooda_seed_event_id))


def handler(data, context):
    try:
        logger.info(pformat(data))
        event_body = json.loads(data['body'])

        logger.info(pformat(event_body))
        if not (verify_token(event_body.get('token')) or environment == 'local'):
            sys.exit()

        if event_body.get('challenge'):
            logger.info('Responding to challenge with {}'.format(event_body.get('challenge')))
            return {'statusCode': 200, 'body': event_body.get('challenge')}

        # post_to_slack({})
        # logger.info(get_all_items())

        return {'statusCode': 200}

    except Exception as e:
        logging.exception(e)
        return {'statusCode': 500, 'body': 'Error in lambda proxy'}


def parse_event(body):
    return


def post_to_slack(body):
    if not body:
        body = {
            'text': 'Cakebot test message from app in {}'.format(environment)
        }

    res = requests.post(slack_webhook_url, data=json.dumps(body))

    logger.info('Slack post status code: {}'.format(res.statusCode))


def get_all_items():
    day_url = construct_filter_url(
        account_id=fooda_account_id,
        building_id=fooda_building_id,
        date='2018-07-31')
    res = requests.get(day_url, cookies=cookies)

    calendar_soup = BeautifulSoup(res.content, 'html.parser')

    menu_url = calendar_soup.find_all(class_='myfooda-event__restaurant')[0]['href']
    res = requests.get(menu_url)

    menu_soup = BeautifulSoup(res.content, 'html.parser')

    items = []
    for item in menu_soup.find_all(class_='item'):
        item_content = item.find_all(class_='item__content')[0]
        items.append({
            'vendor': item['data-vendor_name'],
            'category': item['data-category'],
            'name': item_content.find_all(class_='item__name')[0].getText(),
            'price': Decimal(item_content.find_all(class_='item__price')[0].getText()[1:])})

    return items


def construct_filter_url(account_id, building_id, meal_period=None, date=None):
    if not date:
        date = datetime.datetime.now().strftime('%Y-%m-%d')
    if not meal_period:
        meal_period = 'Lunch'

    url = ('https://app.fooda.com/my?date={}'.format(date)
           + '&filterable[account_id][]={}'.format(account_id)
           + '&filterable[locations][building_id][]={}'.format(building_id)
           + '&filterable[meal_period]={}'.format(meal_period))

    return url


def verify_token(token):
    try:
        if slack_verification_token == token:
            logger.info('Slack token verified.')
            return True
        else:
            logger.info('Invalid Slack token provided.')
            return False
    except Exception:
        logger.info('No body.token in data object')
        return False


if __name__ == '__main__':
    handler(data={'body': '{\"token\":\"faketoken\",\"challenge\":\"fakechallenge\"}'}, context=None)
