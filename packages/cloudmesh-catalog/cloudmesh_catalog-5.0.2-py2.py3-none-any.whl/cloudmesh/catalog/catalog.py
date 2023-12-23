import glob
from dataclasses import dataclass, field

import yaml
from fastapi import FastAPI

from cloudmesh.common.util import path_expand

# TODO: this is not a stand alone prg
# TODO: needs to use yamldb instead of pickle
# TODO: needs to read form defined relative directory for data
#    find data from source deployment while looking for cloudmesh/catalog/data
# TODO: the data directory is in home dire and therefore could be overwritten,
#   we need to moe likely elsewhere
# TODO: the version is hardcoded
# TODO: the initializer of where the data dire is is incorrect, it requires
#   this to be
#      started from dir in which data dir is
# TODO: if yamldb can be used its much more comfortable
# Option:       alternatively we could use containers and Mongo db or something
#               like that
# TODO: if name must be removed

catalog_api_version = "1.0"
catalog_api_base = f"/cloudmesh/{catalog_api_version}/catalog/"


# TODO: is there a way to just set the base url and than all following urls are
#       specified without the baseURL

#
# TODO: why is his not in the class?
#
@app.get("/cloudmesh/v1-0/catalog/{name}")
async def get_name(name):
    """
    Get information about a catalog entry by name.

    Args:
        name (str): The name of the catalog entry.

    Returns:
        dict: The catalog entry information.
    """
    catalog = Catalog('data/')
    entry = catalog.query({'name': name})
    return entry


class Catalog:
    """
    Catalog Class

    This class represents a catalog and provides methods for querying and managing catalog entries.

    Attributes:
        - app (FastAPI): FastAPI instance for serving catalog queries.
        - directory (str): Path to the directory containing catalog data.
        - data (dict): Dictionary containing catalog data.

    Methods:
        - server(): Start the FastAPI server.
        - query(search): Conduct a query using jmsepath.
        - add(file): Add a YAML file to the catalog's data.
        - load(directory=None): Load data using YAML files in the given directory.

    Usage:
        catalog_instance = Catalog('data/')
        catalog_instance.server()

        query_result = catalog_instance.query({'name': 'Amazon Comprehend'})
        print(query_result)
    """


    def __init__(self, directory):
        """
        Initialize the Catalog class.

        Args:
            directory (str): Path to the directory containing catalog data.

        Returns:
            None
        """
        self.server()
        raise NotImplementedError

        # TODO: WE SHOUlD JUST USE dATAbASE AND MAKE SURE WE FIX THAT CLASS

        # self.directory = directory  # string (i.e., 'data/')
        # self.data = {}  # dictionary
        # self.load(directory)  # loads self.data using yaml files in the given directory

    def server(self):
        """
        Start the FastAPI server.

        Args:
            None

        Returns:
            None
        """
        self.app = FastAPI()

    # takes a query in the form {'name': name}, i.e. {'name': 'Amazon Comprehend'}
    # search : dict
    def query(self, search):
        """
        Conduct a query using jmsepath.

        Args:
            search (dict): Dictionary representing the query.

        Returns:
            dict or None: Query result or None if there is an error.
        """
        raise NotImplementedError
        return None

    def add(self, file):
        """
         Add a YAML file to this catalog's self.data.

         Args:
             file (str): The filename. Example: '~/data/amazon_comprehend.yaml'.

         Returns:
             bool: True if the upload was successful.
         """
        file = path_expand(file)
        with open(file, "r") as stream:
            try:
                parsed_yaml = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        self.data.update(parsed_yaml)  # update self.data with data from new file
        raise NotImplementedError

    # loads self.data using yaml files in the given directory
    # directory : string (i.e., 'data/')
    def load(self, directory=None):
        """
        Load data using YAML files in the given directory.

        Args:
            directory (str): Path to the directory. Default is None, and self.directory is used.

        Returns:
            None
        """
        if directory is None:
            directory = self.directory
        files = glob.glob(directory + '*.yaml')  # gets list of yaml files in given directory
        for file in files:
            self.add(file)


@dataclass
class CatalogEntry:
    """
    CatalogEntry Dataclass

    This dataclass represents a catalog entry.

    Attributes:
        - id (str): UUID, globally unique.
        - name (str): Name of the service.
        - author (str): Author of the service.
        - slug (str): Slugline of the service (i.e., amazon-comprehend).
        - title (str): Human-readable title.
        - public (bool): True if public (needs use case to delineate what pub private means).
        - description (str): Human-readable short description of the service.
        - version (str): The version number or tag of the service.
        - license (str): The license description.
        - microservice (str): yes/no/mixed.
        - protocol (str): e.g., REST.
        - owner (str): Name of the distributing entity, organization, or individual. It could be a vendor.
        - modified (str): Modification timestamp (when unmodified, same as created).
        - created (str): Date on which the entry was first created.
        - documentation (str): Link to documentation/detailed description of service (default is 'unknown').
        - source (str): Link to the source code if available (default is 'unknown').
        - tags (list): Human-readable common tags associated with the service (default is an empty list).
        - categories (list): A category that this service belongs to (NLP, Finance, …) (default is an empty list).
        - specification (str): Pointer to where the schema is located (default is 'unknown').
        - additional_metadata (str): Additional metadata pointer (default is 'unknown').
        - endpoint (str): The endpoint of the service (default is 'unknown').
        - sla (str): SLA/Cost: service level agreement including cost (default is 'unknown').
        - authors (str): Contact details of the people or organization responsible for the service (default is 'unknown').
        - data (str): Description of how data is managed (default is 'unknown').

    Usage:
        entry = CatalogEntry(id='123', name='Service Name', author='John Doe', ...)

    """
    # UUID, globally unique
    id: str
    # Name of the service
    name: str
    # Author of the service
    author: str
    # slugline of the service (i.e., amazon-comprehend)
    slug: str
    # Human readable title
    title: str
    # True if public (needs use case to delineate what pub private means)
    public: bool
    # Human readable short description of the service
    description: str
    # The version number or tag of the service
    version: str
    # The license description
    license: str
    # yes/no/mixed
    microservice: str
    # e.g., REST
    protocol: str
    # Name of the distributing entity, organization or individual. It could be a vendor.
    owner: str
    # Modification timestamp (when unmodified, same as created)
    modified: str
    # Date on which the entry was first created
    created: str
    # Link to documentation/detailed description of service
    documentation: str = 'unknown'
    # Link to the source code if available
    source: str = 'unknown'
    # Human readable common tags that are used to identify the service that are associated with the service
    tags: list = field(default_factory=list)
    # A category that this service belongs to (NLP, Finance, …)
    categories: list = field(default_factory=list)
    # specification/schema: pointer to where schema is located
    specification: str = 'unknown'
    # Additional metadata: Pointer to where additional is located including the one here
    additional_metadata: str = 'unknown'
    # The endpoint of the service
    endpoint: str = 'unknown'
    # SLA/Cost: service level agreement including cost
    sla: str = 'unknown'
    # contact details of the people or organization responsible for the service (freeform string)
    authors: str = 'unknown'
    # description on how data is managed
    data: str = 'unknown'

# FOR TESTING
# if __name__ == "__main__":
#    catalog = Catalog('data/catalog/')
#    # print(cat.data)
#
#    query_result = catalog.query({'name': 'Amazon Comprehend'})
#    print(query_result)
