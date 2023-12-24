import json
import unittest
from dataclasses import dataclass, asdict
from decimal import Decimal
from http import HTTPStatus

from capsphere.common import utils
from capsphere.data.api.aws.lambdas.response import ApiGwResponse


@dataclass
class MockObject:
    key: str
    dec_val: Decimal

    def to_dict(self):
        response_dict = asdict(self)
        return response_dict

    def to_json(self):
        return utils.to_json(self.to_dict())


class TestResponse(unittest.TestCase):
    def test_apigw_response(self):
        mock_object = MockObject(key='some_key', dec_val=Decimal(1000.00))
        mock_object_json = mock_object.to_json()
        apigw_resp = ApiGwResponse(statusCode=HTTPStatus.OK.value, headers=None,
                                   body=mock_object_json)
        apigw_resp_dict = apigw_resp.to_dict()
        self.assertEqual(str, type(mock_object.key))
        self.assertEqual(Decimal, type(mock_object.dec_val))
        self.assertEqual(dict, type(apigw_resp_dict))
