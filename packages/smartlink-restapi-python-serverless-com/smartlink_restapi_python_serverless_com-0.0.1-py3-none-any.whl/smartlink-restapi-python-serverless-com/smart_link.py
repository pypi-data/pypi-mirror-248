from circles_local_database_python.generic_crud import GenericCRUD
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from message_local.Recipient import Recipient
from queue_worker_local.queue_worker import QueueWorker

from .utils import generate_random_string

SMART_LINK_COMPONENT_ID = 258
SMART_LINK_COMPONENT_NAME = "smartlink"
DEVELOPER_EMAIL = "akiva.s@circ.zone"
object1 = {
    'component_id': SMART_LINK_COMPONENT_ID,
    'component_name': SMART_LINK_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
logger = Logger.create_logger(object=object1)

SMART_LINK_LENGTH = 20  # (26*2 + 10) ^ 20 = 62^20 possibilities (number with 36 digits)
VERIFY_MAIL_ACTION_ID = 1  # TODO: replace with the real action id


class SmartLinkLocal(GenericCRUD):
    def __init__(self) -> None:
        super().__init__(default_schema_name="smartlink",
                         default_table_name="smartlink_table",
                         default_view_table_name="smartlink_view",
                         default_id_column_name="magic_link_id")

    # We use primitive types for parameters and return value because we want to be able to call this function from srvls
    def insert(self, from_recipient: dict, to_recipient: dict, campaign_id: int, action_id: int) -> int:
        # TODO should have an expiration parameter with a default of 7 days in case of email invitation,
        #  a few hours for sending pin code
        # TODO add support of multiple criteria per campaign
        logger.start()
        from_recipient = Recipient.from_json(from_recipient)
        to_recipient = Recipient.from_json(to_recipient)

        smart_link_id = generate_random_string(length=SMART_LINK_LENGTH)
        # smart_link = f"www.circ.zone?a={smart_link_id}"
        data_json = {
            "smartlink_identifier": smart_link_id,
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

        logger.end(object={"data_json": data_json, "inserted_id": inserted_id})
        return inserted_id

    # REST API GET request with GET parameter id=GsMgEP7rQJWRZUNWV4ES which executes a function based on action_id
    # from action_table with all fields that are not null in starlink_table (similar to queue worker but sync)
    # and get back from the action json with return-code, redirection url, stdout, stderr...
    # call api_management.incoming_api() which will call api_call.insert()

    def execute(self, smartlink_identification: str):
        # TODO: test
        logger.start()
        results = self.select_one_dict_by_id(id_column_name="identification",
                                             id_column_value=smartlink_identification)
        if not results:
            logger.error(message=f"smart_link_id {smartlink_identification} not found")
            return

        action_to_parameters = {
            VERIFY_MAIL_ACTION_ID: {"function_parameters_json": {"to_email": results["to_email"]},
                                    "class_parameters_json": {}},
            # ...
        }
        if results["action_id"] not in action_to_parameters:
            logger.error(message=f"action_id {results['action_id']} not found")
            return
        execution_details = {
            "action_id": results["action_id"],
            "smart_link_id": smartlink_identification,
            "function_parameters_json": action_to_parameters[results["action_id"]]["function_parameters_json"],
            "class_parameters_json": action_to_parameters[results["action_id"]]["class_parameters_json"]
        }
        # TODO: save redirection url (how?)
        QueueWorker(schema_name="smartlink", table_name="smartlink_table", id_column_name="smart_link_id").execute(
            execution_details=execution_details, install_packages=False)

        logger.end()

    # 2. REST API POST gets json with all the details of a specific identifier for Dialog Workflow Remote
    def get_smartlink_details(self, smartlink_identification: str) -> dict:
        logger.start()
        results = self.select_one_dict_by_id(id_column_name="identification",
                                             id_column_value=smartlink_identification)
        if not results:
            logger.error(message=f"smart_link_id {smartlink_identification} not found")
            return {}

        logger.end(object={"results": results})
        return results

    def verify_mail(self, to_email: str):
        print("verify_mail " + to_email)
        pass
