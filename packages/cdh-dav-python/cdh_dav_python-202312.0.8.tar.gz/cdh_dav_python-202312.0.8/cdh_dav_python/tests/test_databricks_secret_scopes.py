import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cdh_dav_python.databricks_service.secret_scope as cdc_secret_scope


class TestSecretScope:
    def test_list_secret_scopes(self, mocker):
        # Mock the dbutils object
        dbutils_mock = mocker.Mock()
        dbutils_mock.secrets.listScopes.return_value = ["scope1", "scope2", "scope3"]

        # Create an instance of SecretScope
        secret_scope = cdc_secret_scope.SecretScope()

        # Call the function under test
        result = secret_scope.list_secret_scopes(dbutils_mock)

        # Assert the result
        assert result == ["scope1", "scope2", "scope3"]
        dbutils_mock.secrets.listScopes.assert_called_once
