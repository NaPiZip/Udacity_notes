import json
import os
import base64

import pytest

from tests.unit import helper

from hello_world import app
from hello_world import transform


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""
    image_file = "hello_world/example.png"
    json_payload = transform.encode_to_json(image_file)

    return {
        "body": json_payload,
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": {"foo": "bar"},
        "headers": {
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch",
        },
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": "GET",
        "stageVariables": {"baz": "qux"},
        "path": "/examplepath",
    }

def test_image_to_json_and_back(apigw_event, mocker):
    image_file = "hello_world/example.png"

    with open(image_file, 'rb') as fid:
        raw_image_data = fid.read()

    json_payload = transform.encode_to_json(image_file)
    decoded_data = transform.decode_from_json(json_payload)
        
    assert(raw_image_data == decoded_data)

def test_trivial_write_and_read(apigw_event, mocker):
    image_file  = "tests/unit/example.png"
    json_file   = "tests/unit/example.json"

    json_payload = transform.encode_to_json(image_file)

    helper.save_json_to_file(json_payload , json_file)
    json_file_content = helper.read_json_from_file(json_file)

    assert(json_file_content == json_payload)

def test_lambda_handler(apigw_event, mocker):
    app.check_output = mocker.MagicMock(return_value=b'G Tesseract OCR')

    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "result" in ret["body"]    
    assert("Tesseract" in data["result"])

def test_dev(apigw_event):
    print(apigw_event['body'])