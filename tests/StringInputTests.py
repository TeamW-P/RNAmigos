import unittest
import json
import os
from .constants.TestPayload import *
from .constants.TestEnvironment import *
from app import app
import io

CURRENT_DIRECTORY = os.path.dirname(__file__)


class StringInputTests(unittest.TestCase):
    '''
    Implements unit testing for the string input endpoint.
    '''

    def setUp(self):
        self.app = app.test_client()

    def test_success_graph_no_lib(self):
        '''
        Tests for a successful run of RNAMigos provided with a single graph and no custom library.
        '''
        payload = STRING_INPUT_GRAPH_NO_LIB
        headers = {}

        response = self.app.post(
            STRING_URL, content_type='multipart/form-data', headers=headers, data=payload)
        with open(os.path.join(CURRENT_DIRECTORY, "responses/RESPONSE_STRING_INPUT_GRAPH_NO_LIB.json")) as f:
            expected_response = json.load(f)
        f.close()
        
        self.assertEqual(200, response.status_code)
        self.assertEqual("graphs" in expected_response,
                         "graphs" in response.json)
        self.assertEqual("rnamigos_library" not in expected_response,
                        "rnamigos_library" not in response.json)
        self.assertEqual("hits" in expected_response["graphs"]["48"],
                         "hits" in response.json["graphs"]["48"])

    def test_success_graphs_no_lib(self):
        '''
        Tests for a successful run of RNAMigos provided with multiple graphs and no custom library.
        '''
        payload = STRING_INPUT_GRAPHS_NO_LIB
        headers = {}

        response = self.app.post(
            STRING_URL, content_type='multipart/form-data', headers=headers, data=payload)
        with open(os.path.join(CURRENT_DIRECTORY, "responses/RESPONSE_STRING_INPUT_GRAPHS_NO_LIB.json")) as f:
            expected_response = json.load(f)
        f.close()
        
        self.assertEqual(200, response.status_code)
        self.assertEqual("graphs" in expected_response,
                         "graphs" in response.json)
        self.assertEqual("rnamigos_library" not in expected_response,
                        "rnamigos_library" not in response.json)
        self.assertEqual("hits" in expected_response["graphs"]["36"],
                         "hits" in response.json["graphs"]["36"])

    def test_success_graph_lib(self):
        '''
        Tests for a successful run of RNAMigos provided with a single graph and a custom library.
        '''
        payload = STRING_INPUT_GRAPH_LIB
        headers = {}

        with open(os.path.join(CURRENT_DIRECTORY, "data/rnamigos_custom_library.txt"), mode="rb") as f1:
            payload["library"] = f1
            response = self.app.post(
                STRING_URL, content_type='multipart/form-data', headers=headers, data=payload)
            with open(os.path.join(CURRENT_DIRECTORY, "responses/RESPONSE_STRING_INPUT_GRAPH_LIB.json")) as f:
                expected_response = json.load(f)
        
        
            self.assertEqual(200, response.status_code)
            self.assertEqual("graphs" in expected_response,
                            "graphs" in response.json)
            self.assertEqual("rnamigos_library" in expected_response,
                            "rnamigos_library" in response.json)
            self.assertEqual("hits" in expected_response["graphs"]["48"],
                            "hits" in response.json["graphs"]["48"])
    
    def test_success_empty_graph_no_lib(self):
        '''
        Tests for a successful run of RNAMigos provided with a single empty graph and no custom library.
        '''
        payload = STRING_INPUT_EMPTY_GRAPH_NO_LIB
        headers = {}

        response = self.app.post(
            STRING_URL, content_type='multipart/form-data', headers=headers, data=payload)
        with open(os.path.join(CURRENT_DIRECTORY, "responses/RESPONSE_STRING_INPUT_EMPTY_GRAPH_NO_LIB.json")) as f:
            expected_response = json.load(f)
        f.close()
        
        self.assertEqual(200, response.status_code)
        self.assertEqual('graphs' in expected_response,
                         'graphs' in response.json)

    def test_fail_graph_invalid_lib(self):
        '''
        Tests for a failed run of RNAMigos provided with a single graph and invalid custom library (non .txt)
        '''
        payload = STRING_INPUT_GRAPH_LIB
        headers = {}

        with open(os.path.join(CURRENT_DIRECTORY, "data/rnamigos_custom_library.jpg"), mode="rb") as f1:
            payload["library"] = f1
            response = self.app.post(
                STRING_URL, content_type='multipart/form-data', headers=headers, data=payload)
            with open(os.path.join(CURRENT_DIRECTORY, "responses/RESPONSE_STRING_INPUT_GRAPH_INVALID_LIB.json")) as f:
                expected_response = json.load(f)
        
        
        self.assertEqual(400, response.status_code)
        self.assertEqual("error" in expected_response,
                         "error" in response.json)

    def test_fail_invalid_graph_no_lib(self):
        '''
        Tests for a failed run of RNAMigos provided with a single invalid graph and no custom library.
        '''
        payload = STRING_INPUT_INVALID_GRAPH_NO_LIB
        headers = {}

        response = self.app.post(
            STRING_URL, content_type='multipart/form-data', headers=headers, data=payload)
        with open(os.path.join(CURRENT_DIRECTORY, "responses/RESPONSE_STRING_INPUT_INVALID_GRAPH_NO_LIB.json")) as f:
            expected_response = json.load(f)
        f.close()
        
        self.assertEqual(400, response.status_code)
        self.assertEqual("error" in expected_response,
                         "error" in response.json)
    
    def test_fail_graph_empty_lib(self):
        '''
        Tests for a failed run of RNAMigos provided with a single graph and an empty custom library.
        '''
        payload = STRING_INPUT_GRAPH_LIB
        headers = {}

        with open(os.path.join(CURRENT_DIRECTORY, "data/empty_rnamigos_custom_library.txt"), mode="rb") as f1:
            payload["library"] = f1
            response = self.app.post(
                STRING_URL, content_type='multipart/form-data', headers=headers, data=payload)
            with open(os.path.join(CURRENT_DIRECTORY, "responses/RESPONSE_STRING_INPUT_GRAPH_EMPTY_LIB.json")) as f:
                expected_response = json.load(f)
        
        self.assertEqual(400, response.status_code)
        self.assertEqual("error" in expected_response,
                         "error" in response.json)
                         