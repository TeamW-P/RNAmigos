import unittest
import json
import os
from .constants.TestPayload import *
from .constants.TestEnvironment import *
# relative paths refuse to work because Python is terrible!
from app import app

CURRENT_DIRECTORY = os.path.dirname(__file__)

# IMPORTANT NOTE: BP Results are not deterministic. To that effect, these tests validate the existence of keys and whether responses are successful or a failure
# NOTE: For boolean based comparisons, we still use assertEquals so there is no need to update code in the case of a new response (i.e. you only need to change the expected response JSONs)


class StringInputTests(unittest.TestCase):
    '''
    Implements unit testing for the string input endpoint.
    '''

    def setUp(self):
        self.app = app.test_client()

    def test_successful_graph_no_lib(self):
        '''
        Tests for a successful run of BayesPairing where a sequence, and no secondary structure are provided.
        '''
        payload = STRING_INPUT_WITH_GRAPH_NO_LIB
        headers = {}

        response = self.app.post(
            STRING_URL, content_type='multipart/form-data', headers=headers, data=payload)
        with open(os.path.join(CURRENT_DIRECTORY, "responses/RESPONSE_STRING_INPUT_WITH_GRAPH_NO_BIB.json")) as f:
            expected_response = json.load(f)
        f.close()
        
        self.assertEqual(200, response.status_code)
        self.assertEqual("graphs" in expected_response,
                         "graphs" in response.json)
        self.assertEqual("hits" in expected_response["graphs"]["36"],
                         "hits" in response.json["graphs"]["36"])