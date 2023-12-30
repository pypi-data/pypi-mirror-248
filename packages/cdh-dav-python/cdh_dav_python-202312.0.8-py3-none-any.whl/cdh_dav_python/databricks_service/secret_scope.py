# spark
from pyspark.sql import SparkSession

import requests
import sys, os
import json

OS_NAME = os.name
sys.path.append("../..")


class SecretScope:
    """
    A class that provides methods to interact with secret scopes in Databricks.
    """

    @classmethod
    def list_secret_scopes(cls, dbutils):
        """
        Lists all the secret scopes in Databricks.

        Parameters:
        - dbutils: The dbutils object used to interact with Databricks.

        Returns:
        - secret_scopes: A list of secret scopes.
        """
        running_local = ("dbutils" in locals() or "dbutils" in globals()) is not True

        if running_local is True:
            spark = SparkSession.builder.appName("cdc_data_ecosystem").getOrCreate()

        secret_scopes = dbutils.secrets.listScopes()
        return secret_scopes
