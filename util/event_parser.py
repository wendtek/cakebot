from bs4 import BeautifulSoup
import requests
from datetime import datetime, time, date, timedelta
import calendar
from pytz import timezone
from urllib.parse import quote
from pprint import pprint, pformat
from decimal import Decimal
import logging
import sys
import json
from util.config import config

cookies = {}
cookies['context'] = quote(
    '{{"entity":"select_event","id":"{0}"}}'.format(config['fooda_seed_event_id']))
central = timezone('US/Central')

def generate_response(body):
    now = datetime.now(central)

    items = get_all_items(next_delivery_date(now))
    tree_fiddy = sorted(filter_items(items, max=Decimal(3.50)), key=lambda item: item['vendor'])

    response_text = '\n'.join(['{} from {} for ${}'.format(
                        item['name'],
                        item['vendor'],
                        item['price']) for item in tree_fiddy if item['category'] == 'Desserts'])

    return response_text


def filter_items(items, min=Decimal(0), max=Decimal(1337)):
    new_items = [ item for item in items if min <= item['price'] <= max ]
    return new_items


def next_delivery_date(dt):
    if dt.time() < time(hour=10, minute=0) and dt.weekday() in [0, 1, 2, 3]:
        print(dt.strftime('%Y-%m-%d'))
        return dt.strftime('%Y-%m-%d')
    else:
        return next_delivery_date((dt + timedelta(days=1)).replace(hour=8, minute=0))


def get_all_items(date_string):
    day_url = construct_filter_url(
        account_id=config['fooda_account_id'],
        building_id=config['fooda_building_id'],
        date_string=date_string)
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


def construct_filter_url(account_id, building_id, meal_period=None, date_string=None):
    if not date_string:
        date_string = datetime.now().strftime('%Y-%m-%d')
    if not meal_period:
        meal_period = 'Lunch'

    url = ('https://app.fooda.com/my?date={}'.format(date_string)
           + '&filterable[account_id][]={}'.format(account_id)
           + '&filterable[locations][building_id][]={}'.format(building_id)
           + '&filterable[meal_period]={}'.format(meal_period))

    return url
