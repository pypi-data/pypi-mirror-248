"""Initialize the cdc_tech_environment_service subpackage of cdh_dav_python package"""

# allow absolute import from the root folder
# whatever its name is.

import sys  # don't remove required for error handling
import os

# Import from sibling directory ..\cdc_tech_environment_service
OS_NAME = os.name

sys.path.append("..")

if OS_NAME.lower() == "nt":
    print("cdc_tech_environment_service: windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..\\..")))
else:
    print("cdc_tech_environment_service: non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))

import cdh_dav_python.az_storage_service.az_storage_queue
import cdh_dav_python.cdc_tech_environment_service.job_core
import cdh_dav_python.cdc_tech_environment_service.repo_core
import cdh_dav_python.cdc_security_service.security_core
import cdh_dav_python.cdc_admin_service.environment_logging
import cdh_dav_python.cdc_tech_environment_service.environment_spark
import cdh_dav_python.cdc_tech_environment_service.environment_file
import cdh_dav_python.cdc_tech_environment_service.environment_core
import cdh_dav_python.cdc_tech_environment_service.environment_http
