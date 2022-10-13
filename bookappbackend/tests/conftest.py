"""
    Pytest configuration
"""

# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# Needed for making pytest fixtures work correctly
# pylint: disable=wrong-import-position

import os
import pathlib
from threading import Thread

from bookappbackend.tests.fixtures import *

# set the current working dir
os.chdir(f"{pathlib.Path(__file__).parent.parent.parent}")

# delete old database
if os.path.isfile("bookappbackend/tests/test.db"):
    os.remove("bookappbackend/tests/test.db")

# import needed modules
from bookappbackend.database.db_manager import DBManager

# set the test database file path
DBManager.dbfile_path = "bookappbackend/tests/test.db"

# mport main module
import main

# start the server
Thread(target=main.main, daemon=True).start()

# pylint: enable=wrong-import-position
