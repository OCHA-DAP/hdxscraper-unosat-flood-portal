#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import requests

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import config.load as Config
from utilities.db import CleanTable
from utilities.db import StoreRecords
from utilities.prompt_format import item


def FetchData(url=Config.LoadConfig()[0]['url']):
  '''Fetching data from the UNOSAT API.'''

  #
  # Loading main URL from the config
  # file and making request.
  #
  try:
    u = url
    r = requests.get(u)

  except Exception as e:
    print '%s Could not connect to url: %s' % (item('prompt_error'), url)
    print e
    return False

  #
  # Checking the status code.
  #
  if r.status_code != requests.codes.ok:
    print '%s Request to UNOSAT servers failed to complete.' % item('propmt_error')
    return False

  else:
    return r.json()


def DownloadAndProcessData():
  '''Process UNOSAT output data.'''

  #
  # Loading data.
  #
  data = FetchData()
  if data == False:
    return False

  #
  # Processing data.
  #
  record_array = []
  for record in data['records']:
    for link in record['links']:
      processed_record = {
        'title': record['title'],
        'id': record['id'],
        'updated': record['updated'],
        'summary': record['summary'],
        'created': None,
        'country': None,
        'link_href': link['href'],
        'link_type': link['type']
      }
      record_array.append(processed_record)


  return record_array


def StoreData(data, table_name, verbose=True):
  '''Storing data in database.'''

  #
  # Cleaning table.
  #
  CleanTable(table_name)

  #
  # Fetching keys from
  # one of the records and
  # storing data in database.
  #
  try:
    table_schema = data[0].keys()
    StoreRecords(schema=table_schema, data=data, table=table_name)

  except Exception as e:
    print e
    return False


def Main(write_json=False):
  '''Wrapper.'''
  try:
    d = DownloadAndProcessData()

    if write_json:
      import json
      with open('data/test.json', 'w') as outfile:
          json.dump(d, outfile)

    StoreData(data=d, table_name='unprocessed_data')
    print '%s Successfully fetched %s records from the UNOSAT Flood Portal.\n' % (item('prompt_success'), len(d))

  except Exception as e:
    print e
    return False


if __name__ == '__main__':
  Main()