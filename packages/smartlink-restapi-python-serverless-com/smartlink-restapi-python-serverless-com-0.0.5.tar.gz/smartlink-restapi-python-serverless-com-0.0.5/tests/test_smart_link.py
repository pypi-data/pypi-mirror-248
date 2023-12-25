# TODO: add serverless test
import os
import sys

from message_local.Recipient import Recipient

script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))
from src.smartlink import SmartLinkLocal  # noqa: E402
from src.utils import generate_random_string  # noqa: E402

smartlink = SmartLinkLocal()
from_recipient = Recipient(user_id=1, contact_id=2,
                           email_address="test@gmail.com", preferred_language="en")  # those don't matter
to_recipient = Recipient(person_id=1, telephone_number="0501234567", preferred_language="en")


def test_generate_random_string():
    result = generate_random_string(length=10)
    assert len(result) == 10

    result = generate_random_string(length=20)
    assert len(result) == 20


def test_insert():
    inserted_id = smartlink.insert(from_recipient=from_recipient.to_json(),
                                    to_recipient=to_recipient.to_json(),
                                    campaign_id=1, action_id=1)
    assert inserted_id > 0  # no error
