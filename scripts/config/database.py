#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import scraperwiki
import load as Config

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

from os import path as p
from utilities.prompt_format import item


def CreateTables(config_path=Config.DEV_CONFIG_PATH, verbose=True):
  '''Creating the tables of the new database.'''

  #
  # Load configuration data.
  #
  try:
    config_data = Config.LoadConfig(config_path)['database']

  except Exception as e:
    if verbose:
      print '%s Could not load configuration file.' % item('prompt_error')
      print e

    return False

  #
  # Create SQL statements for every table.
  #
  sql_statements = {}

  for endpoint in config_data:
    table_name = endpoint['database']['table_name']
    statement = " TEXT, ".join(endpoint['database']['fields'])
    statement = 'CREATE TABLE IF NOT EXISTS %s(%s TEXT)' % (table_name, statement)
    sql_statements[table_name] = statement

  for table in sql_statements:
    scraperwiki.sqlite.execute(sql_statements[table])
    print "%s Table `%s` created." % (item('prompt_bullet'), str(table))

  #
  ## I'm unable to test the following chunk.
  ## As a result, it will remain commented
  ## below.
  #
  # for table in sql_statements:
  #   try:
  #     scraperwiki.sqlite.execute(sql_statements[table])
  #     print "%s Table `%s` created." % (item('prompt_bullet'), str(table))

  #   except Exception as e:
  #     if verbose:
  #       print '%s Failed to create table %s.' % (item('prompt_error'), table_name)
  #       print e
  #     return False

  print "%s Database created successfully.\n" % item('prompt_success')
  return True


def Main():
  '''Wrapper function.'''

  CreateTables()


if __name__ == '__main__':
  Main()
