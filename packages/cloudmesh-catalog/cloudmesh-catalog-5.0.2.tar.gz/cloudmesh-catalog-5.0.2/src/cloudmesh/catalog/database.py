from yamldb import YamlDB
# from cloudmesh.common.util import path_expand

class DataBase(YamlDB):
    """
    DataBase Class

    This class extends the YamlDB class and provides additional functionality for handling a catalog database.

    Methods:
        - __init__(name="~/.cloudmesh/catalog/data.yaml", kind=YamlDB): Initializes the DataBase instance.
        - update(name): Updates the database with the specified name.

    Attributes:
        - db: An instance of the YamlDB class representing the database.

    Usage:
        db = DataBase(name='path/to/data.yaml', kind=YamlDB)
        db.update('entry_name')
    """

    def __init__(self, name="~/.cloudmesh/catalog/data.yaml", kind=YamlDB):
        """
        Initializes the DataBase instance.

        Args:
            name (str): The path to the database file.
            kind (class): The class representing the database.

        Returns:
            None
        """
        self.db = YamlDB(filename=name)
        # self.db = YamlDB(filename=path_expand(name))
        #
        # TODO: create the database if it does not exists
        # check if yamldb already does this
        #

    def update(self, name):
        """
        Updates the database with the specified name.

        Args:
            name (str): The name of the entry to be updated.

        Returns:
            None
        """
        self.db.uppdate(name)
