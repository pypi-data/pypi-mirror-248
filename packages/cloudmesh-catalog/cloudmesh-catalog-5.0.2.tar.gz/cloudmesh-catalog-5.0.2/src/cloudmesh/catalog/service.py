"""
Cloudmesh Catalog FastAPI Service

This FastAPI service provides RESTful APIs to interact with the Cloudmesh Catalog.

- Root Endpoint:
  - `/`: Indicates the service is running.

- List Database Endpoint:
  - `/list`: Lists the content of the catalog database.

- Load Directory Endpoint:
  - `/load/{directory}`: Loads YAML files from the specified directory into the catalog database.

- Read Item Endpoint:
  - `/items/{item_id}`: Reads an item from the catalog database.

The service also automatically updates its catalog database by searching for YAML files
in the specified source directory during startup.

Note: The database file location and source directory are set in the script and can be adjusted accordingly.
"""
from fastapi import FastAPI
from yamldb import YamlDB
from cloudmesh.common.util import path_expand
import yamldb
from cloudmesh.common.util import path_expand
from pathlib import Path
from pprint import pprint

app = FastAPI()

filename = path_expand("~/.cloudmesh/catalog/data.yml")
print (filename)
print(yamldb.__version__)

db = yamldb.YamlDB(filename=filename)

#
# PATH NEEDS TO BE DONE DIFFERENTLY, probably as parameter to start.
# see also load command
source = path_expand("~/Desktop/cm/nist/catalog")

def _find_sources_from_dir(source=None):
    """
    Finds YAML sources in the specified directory.

    Args:
        source (str): The directory to search for YAML files.

    Returns:
        Iterator[Path]: An iterator over the YAML files found.
    """
    source = Path(source).resolve()
    result = Path(source).rglob('*.yaml')
    return result

files = _find_sources_from_dir(source=source)

for file in files:
    db.update(file)

@app.get("/")
def read_root():
    """
    Root endpoint.

    Returns:
        dict: A dictionary indicating the service is running.
    """
    return {"Cloudmesh Catalog": "running"}

@app.get("/list")
def list_db():
    """
    Lists the content of the catalog database.

    Returns:
        YamlDB: The catalog database content.
    """
    return db

@app.get("/load/{directory}")
def load(directory: str):
    """
    Loads YAML files from the specified directory into the catalog database.

    Args:
        directory (str): The directory containing YAML files.

    Returns:
        dict: A dictionary indicating the loaded directory.
    """
    return {"Cloudmesh Catalog": directory}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    """
    Reads an item from the catalog database.

    Args:
        item_id (int): The ID of the item to read.

    Returns:
        dict: A dictionary with the item ID.
    """
    return {"item_id": item_id}
