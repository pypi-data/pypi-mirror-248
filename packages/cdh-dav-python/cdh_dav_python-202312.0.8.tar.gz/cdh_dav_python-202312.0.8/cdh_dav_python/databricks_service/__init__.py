"""Initialize the alation_service subpackage of cdh_dav_python package"""
# allow absolute import from the root folder
# whatever its name is.
# from cdh_dav_python.az_storage_service import az_storage_queue


import sys  # don't remove required for error handling
import os

from . import notebook
from . import secret_scope
from . import workspace
from . import dataset_crud
from . import dataset_core
from . import dataset_convert
from . import dataset_extract
from . import database

# Import from sibling directory ..\developer_service
OS_NAME = os.name

sys.path.append("..")
if OS_NAME.lower() == "nt":
    print("cdc_metadata_service: windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..\\..")))
else:
    print("cdc_metadata_service: non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))


__all__ = [
    "secret_scope",
    "workspace",
    "notebook",
    "dataset_crud",
    "dataset_core",
    "dataset_convert",
    "dataset_extract",
    "database",
]
