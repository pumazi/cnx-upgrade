# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2013, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
from __future__ import print_function
import os
import sys

import psycopg2


__all__ = ('DB_CONNECTION_STRING', 'TESTING_DATA_DIRECTORY',
           'postgresql_fixture', 'db_connect',
          )


here = os.path.abspath(os.path.dirname(__file__))
_DB_CONNECTION_STRING_ENV_VAR_NAME = 'DB_CONNECTION_STRING'
_DB_CONNECTION_STRING_CLI_OPT_NAME = '--db-conn-str'
try:
    DB_CONNECTION_STRING = os.environ[_DB_CONNECTION_STRING_ENV_VAR_NAME]
except:
    try:
        arg_pos = sys.argv.index(_DB_CONNECTION_STRING_CLI_OPT_NAME)
    except ValueError:
        # Use default...
        print("Using default database connection string.",
              file=sys.stderr)
        DB_CONNECTION_STRING = "dbname=cnxarchive-testing user=cnxarchive password=cnxarchive"
    else:
        DB_CONNECTION_STRING = sys.argv[arg_pos+1]
TESTING_DATA_DIRECTORY = os.path.join(here, 'data')


class PostgresqlFixture:
    """A testing fixture for a live (same as production) SQL database.
    This will set up the database once for a test case. After each test
    case has completed, the database will be cleaned (all tables dropped).

    On a personal note, this seems archaic... Why can't I rollback to a
    transaction?
    """

    def __init__(self):
        # Configure the database connection.
        self.connection_string = DB_CONNECTION_STRING
        # Drop all existing tables from the database.
        self._drop_all()

    def _drop_all(self):
        """Drop all tables in the database."""
        with psycopg2.connect(self.connection_string) as db_connection:
            with db_connection.cursor() as cursor:
                cursor.execute("DROP SCHEMA public CASCADE")
                cursor.execute("CREATE SCHEMA public")

    def setUp(self):
        # Initialize the database schema.
        from cnxarchive.database import initdb
        settings = {'db-connection-string': self.connection_string}
        initdb(settings)

    def tearDown(self):
        # Drop all tables.
        self._drop_all()

postgresql_fixture = PostgresqlFixture()


def db_connect(method):
    """Decorator for methods that need to use the database

    Example:
    @db_connect
    def setUp(self, cursor):
        cursor.execute(some_sql)
        # some other code
    """
    def wrapped(self, *args, **kwargs):
        with psycopg2.connect(DB_CONNECTION_STRING) as db_connection:
            with db_connection.cursor() as cursor:
                return method(self, cursor, *args, **kwargs)
            db_connection.commit()
    return wrapped
