"""
Define db specific type aliases
"""

# Builtin imports
from typing import TypeAlias

# Project specific imports
import pymongo.database

# TypeAlias for MongoDB Database
MongoDatabase: TypeAlias = pymongo.database.Database
