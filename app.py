from bs4 import BeautifulSoup
import requests
import datetime
import os
from urllib.parse import quote
from pprint import pprint
from decimal import Decimal


fooda_account_id = os.environ['FOODA_ACCOUNT_ID']
fooda_building_id = os.environ['FOODA_BUILDING_ID']
fooda_seed_event_id = os.environ['FOODA_SEED_EVENT_ID']
context_template = "{{""entity"":""select_event"",""id"":""{0}""}}"
cookies = {}
cookies['context'] = quote(
    '{{"entity":"select_event","id":"{0}"}}'.format(fooda_seed_event_id))


def handler(event, context):
    day_url = construct_filter_url(
        account_id=fooda_account_id,
        building_id=fooda_building_id,
        date='2018-07-31')
    res = requests.get(day_url, cookies=cookies)

    soup = BeautifulSoup(res.content, 'html.parser')

    menu_url = soup.find_all(class_='myfooda-event__restaurant')[0]['href']
    res = requests.get(menu_url)

    soup = BeautifulSoup(res.content, 'html.parser')

    items = []
    for item in soup.find_all(class_='item'):
        item_content = item.find_all(class_='item__content')[0]
        items.append({
            'vendor': item['data-vendor_name'],
            'category': item['data-category'],
            'name': item_content.find_all(class_='item__name')[0].getText(),
            'price': Decimal(item_content.find_all(class_='item__price')[0].getText()[1:])})

    pprint(items)

    return True


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


if __name__ == '__main__':
    handler({}, None)
