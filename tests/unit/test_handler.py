import json

import pytest

from update_efs_throughputmode import app


@pytest.fixture()
def sns_event():

    return
    {
      "Records": [
        {
          "EventSource": "aws:sns",
          "EventVersion": "1.0",
          "EventSubscriptionArn": "arn:aws:sns:us-east-1::ExampleTopic",
          "Sns": {
            "Type": "Notification",
            "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
            "TopicArn": "arn:aws:sns:us-east-1:123456789012:ExampleTopic",
            "Subject": "example subject",
            "Message": "example message",
            "Timestamp": "1970-01-01T00:00:00.000Z",
            "SignatureVersion": "1",
            "Signature": "EXAMPLE",
            "SigningCertUrl": "EXAMPLE",
            "UnsubscribeUrl": "EXAMPLE",
            "MessageAttributes": {
              "Test": {
                "Type": "String",
                "Value": "TestString"
              },
              "TestBinary": {
                "Type": "Binary",
                "Value": "TestBinary"
              }
            }
          }
        }
      ]
    }

def test_lambda_handler(apigw_event, mocker):

    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "message" in ret["body"]
    assert data["message"] == "hello world"
    # assert "location" in data.dict_keys()
