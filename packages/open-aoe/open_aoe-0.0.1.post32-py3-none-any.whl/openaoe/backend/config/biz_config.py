import sys
import yaml

from openaoe.backend.util.log import log
from .constant import *
import os

logger = log(__name__)


class BizConfig:
    def __init__(self, **args):
        self.__dict__.update(args)

    def get(self, field):
        if field in self.__dict__:
            return self.__dict__[field]
        return None


logger.info("start to init configuration.")
with open(os.path.dirname(__file__) + "/config_test.yaml") as fin:
    m = yaml.safe_load(fin)
    if not m or len(m) == 0:
        logger.error("init configuration failed. Exit")
        sys.exit(-1)

    global biz_config
    biz_config = BizConfig(**m)
logger.info("init configuration successfully.")


def get_configuration(vendor: str, field):
    if biz_config.get(vendor) and biz_config.get(vendor).get(field):
        return biz_config.get(vendor).get(field)

    logger.error(f"vendor: {vendor} has no field: {field} configuration")
    return ""


def get_base_url(vendor: str) -> str:
    return get_configuration(vendor, "api_base")


def get_api_key(vendor: str) -> str:
    return get_configuration(vendor, "api_key")

def app_abs_path():
    return os.path.dirname(os.path.abspath(__file__)).split("/backend")[0]


def img_out_path():
    abs_path = app_abs_path()
    return f'{abs_path}/frontend/dist/tmp/img/out'


def img_in_path():
    abs_path = app_abs_path()
    return f'{abs_path}/frontend/dist/tmp/img/in'