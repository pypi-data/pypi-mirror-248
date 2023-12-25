import os

import requests
import sdk.src.utilities as utilities
from dotenv import load_dotenv
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from url_local.action_name_enum import ActionName
from url_local.component_name_enum import ComponentName
from url_local.entity_name_enum import EntityName
from url_local.url_circlez import OurUrl
from user_context_remote.user_context import UserContext

load_dotenv()

SMARTLINK_COMPONENT_ID = 258
SMARTLINK_COMPONENT_NAME = "smart link remote"
DEVELOPER_EMAIL = "akiva.s@circ.zone"
logger_object = {
    'component_id': SMARTLINK_COMPONENT_ID,
    'component_name': SMARTLINK_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}

SMARTLINK_REMOTE_API_VERSION = 1


class SmartLinkRemote(OurUrl):
    def __init__(self):
        self.logger = Logger.create_logger(object=logger_object)
        self.user_context = UserContext()

    def get_smartlink(self, smartlink_identifier: str) -> requests.Response:
        self.logger.start()
        query_params = {
            "identifier": smartlink_identifier
        }
        response = self._call_response_by_action_name(action_name=ActionName.GET_SMARTLINK_DATA_BY_IDENTIFIER.value,
                                                      query_params=query_params)
        self.logger.end(object={"response": response})
        return response

    def execute_smartlink(self, smartlink_identifier: str) -> requests.Response:
        self.logger.start()
        query_params = {
            "identifier": smartlink_identifier
        }

        response = self._call_response_by_action_name(action_name=ActionName.EXECUTE_SMARTLINK_BY_IDENTIFIER.value,
                                                      query_params=query_params)
        self.logger.end(object=response)
        return response

    def _call_response_by_action_name(self, action_name: str, query_params: dict) -> requests.Response:
        url = self.endpoint_url(
            brand_name=os.getenv("BRAND_NAME"),
            environment_name=os.getenv("ENVIRONMENT_NAME"),
            component_name=ComponentName.SMARTLINK.value,
            entity_name=EntityName.SMARTLINK.value,
            version=SMARTLINK_REMOTE_API_VERSION,
            action_name=action_name,
            query_parameters=query_params
        )

        self.logger.info(url)

        user_jwt = self.user_context.get_user_jwt()
        header = utilities.create_http_headers(user_jwt)
        response = requests.get(url, headers=header)
        return response
