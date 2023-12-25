import json
from http import HTTPStatus

from lambda_decorators import cors_headers
from sdk.src.utilities import create_http_body

from .smartlink import SmartLinkLocal


@cors_headers
# I'm not sure if we are going to use this handler, let's keep it for the future
def execute_smartlink_handler(event, context):
    # TODO Add optional parameter to logger.start()
    #  which called api_call, so logger.start will call api_management
    #  to insert into api_call_table all fields including session_id.

    # get parameters from event
    smartlink_identifier = event.get("identifier")

    SmartLinkLocal().execute(smartlink_identifier=smartlink_identifier)

    body = {
        "message": "Executed smartlink successfully with smartlink_identifier" + smartlink_identifier,
        "input": event
    }

    response = {
        "statusCode": HTTPStatus.OK,
        "body": create_http_body(body)
    }

    return response


@cors_headers
def get_smartlink_details_handler(event, context):
    # get parameters from event
    smartlink_identifier = event.get("identifier")

    smartlink_details = SmartLinkLocal().get_smartlink_details(smartlink_identifier=smartlink_identifier)

    body = {
        "message": "Executed smartlink successfully with smartlink_identifier" + smartlink_identifier,
        "input": event,
        "smartlink_details": smartlink_details
    }

    response = {
        "statusCode": HTTPStatus.OK,
        "body": create_http_body(body)
    }

    return response


@cors_headers
def create_smartlink_handler(event, context):
    from_recipient = json.loads(event.get("from_recipient"))
    to_recipient = json.loads(event.get("to_recipient"))
    campaign_id = event.get("campaign_id")
    action_id = event.get("action_id")

    # create a SmartLink
    inserted_id = SmartLinkLocal().insert(from_recipient=from_recipient, to_recipient=to_recipient,
                                          campaign_id=campaign_id, action_id=action_id)

    body = {
        "message": "Created smartlink successfully with smartlink_identifier" + str(inserted_id),
        "input": event,
        "smartlink_id": inserted_id
    }
    response = {
        "statusCode": HTTPStatus.OK,
        "body": create_http_body(body)
    }

    return response
