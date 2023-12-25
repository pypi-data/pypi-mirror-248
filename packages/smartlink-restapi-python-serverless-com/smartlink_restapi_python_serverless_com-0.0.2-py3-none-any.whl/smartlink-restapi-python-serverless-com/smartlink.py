# from circles_local_database_python.generic_crud import GenericCRUD
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from message_local.Recipient import Recipient
from queue_worker_local.queue_worker import QueueWorker

from .utils import generate_random_string

SMARTLINK_COMPONENT_ID = 258
SMARTLINK_COMPONENT_NAME = "smartlink"
DEVELOPER_EMAIL = "akiva.s@circ.zone"
logger_object = {
    'component_id': SMARTLINK_COMPONENT_ID,
    'component_name': SMARTLINK_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
logger = Logger.create_logger(object=logger_object)

SMARTLINK_LENGTH = 20  # (26*2 + 10) ^ 20 = 62^20 possibilities (number with 36 digits)
VERIFY_EMAIL_ADDRESS_ACTION_ID = 1  # TODO: replace with the real action id


class SmartLinkLocal(QueueWorker):
    def __init__(self) -> None:
        # QueueWorker is a subclass of GenericCRUD.
        # GenericCRUD.__init__(self, default_schema_name="smartlink",
        #                      default_table_name="smartlink_table",
        #                      default_view_table_name="smartlink_view",
        #                      default_id_column_name="magic_link_id")
        QueueWorker.__init__(self, schema_name="smartlink", table_name="smartlink_table", id_column_name="smartlink_id")

    # We use primitive types for parameters and return value because we want to be able to call this function from srvls
    def insert(self, from_recipient: dict, to_recipient: dict, campaign_id: int, action_id: int) -> int:
        # TODO should have an expiration parameter with a default of 7 days in case of email invitation,
        #  a few hours for sending pin code
        # TODO add support of multiple criteria per campaign
        session_id = generate_random_string(length=32)
        logger.start(object={"session_id": session_id,
                             "from_recipient": from_recipient,
                             "to_recipient": to_recipient,
                             "campaign_id": campaign_id,
                             "action_id": action_id})
        from_recipient = Recipient.from_json(from_recipient)
        to_recipient = Recipient.from_json(to_recipient)

        smartlink_identifier = generate_random_string(length=SMARTLINK_LENGTH)
        # smartlink = f"www.circ.zone?a={smartlink_identifier}"
        data_json = {
            "smartlink_identifier": smartlink_identifier,
            "campaign_id": campaign_id,
            "action_id": action_id,
            "from_email": from_recipient.get_email_address(),
            "to_email": to_recipient.get_email_address(),
            "from_normalized_phone": from_recipient.get_canonical_telephone(),
            "to_normalized_phone": to_recipient.get_canonical_telephone(),
            "lang_code": to_recipient.get_preferred_language()
            # TODO: get to_group_id and effective user id
        }
        # contact_id, user_id, person_id, profile_id
        data_json.update({"to_" + key: value for key, value in to_recipient.to_json().items()
                          if key.endswith("_id")})
        data_json.update({"from_" + key: value for key, value in from_recipient.to_json().items()
                          if key.endswith("_id")})
        inserted_id = super().insert(data_json=data_json)

        logger.end(object={"session_id": session_id, "data_json": data_json, "inserted_id": inserted_id})
        return inserted_id

    # REST API GET request with GET parameter id=GsMgEP7rQJWRZUNWV4ES which executes a function based on action_id
    # from action_table with all fields that are not null in starlink_table (similar to queue worker but sync)
    # and get back from the action json with return-code, redirection url, stdout, stderr...
    # call api_management.incoming_api() which will call api_call.insert()

    def execute(self, smartlink_identifier: str):
        # TODO: test
        session_id = generate_random_string(length=32)
        logger.start(object={"session_id": session_id,
                             "smartlink_identifier": smartlink_identifier})
        results = self.select_one_dict_by_id(id_column_name="identification",
                                             id_column_value=smartlink_identifier)
        if not results:
            logger.error(message=f"smartlink_id {smartlink_identifier} not found",
                         object={"session_id": session_id})
            return

        action_to_parameters = {
            VERIFY_EMAIL_ADDRESS_ACTION_ID: {"function_parameters_json": {"to_email": results["to_email"]},
                                             "class_parameters_json": {}},
            # ...
        }
        if results["action_id"] not in action_to_parameters:
            logger.error(message=f"action_id {results['action_id']} not found",
                         object={"session_id": session_id})
            return
        execution_details = {
            "action_id": results["action_id"],
            "smartlink_id": smartlink_identifier,
            "function_parameters_json": action_to_parameters[results["action_id"]]["function_parameters_json"],
            "class_parameters_json": action_to_parameters[results["action_id"]]["class_parameters_json"]
        }
        # TODO: save redirection url (how?)
        super().execute(execution_details=execution_details)

        logger.end(object={"session_id": session_id, "execution_details": execution_details})

    # 2. REST API POST gets json with all the details of a specific identifier for Dialog Workflow Remote
    def get_smartlink_details(self, smartlink_identifier: str) -> dict:
        session_id = generate_random_string(length=32)
        logger.start(object={"session_id": session_id,
                             "smartlink_identifier": smartlink_identifier})
        results = self.select_one_dict_by_id(id_column_name="identification",
                                             id_column_value=smartlink_identifier)
        if not results:
            logger.error(message=f"smartlink_id {smartlink_identifier} not found",
                         object={"session_id": session_id})
            return {}

        logger.end(object={"session_id": session_id, "results": results})
        return results
