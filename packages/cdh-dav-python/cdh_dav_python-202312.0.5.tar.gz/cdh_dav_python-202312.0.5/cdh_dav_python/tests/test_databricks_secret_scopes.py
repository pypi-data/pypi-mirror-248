import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cdh_dav_python.databricks_service.secret_scope as cdc_secret_scope


def test_get_secret_scopes():
    # Call the function under test
    status_code, message = cdc_secret_scope.SecretScope.list_secret_scopes()
