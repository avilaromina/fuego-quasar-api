from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient


TOPSECRET_URL = reverse('transmission:topsecret')
TOPSECRET_SPLIT_KENOBI_URL = reverse('transmission:topsecret_split', kwargs={'name': 'kenobi'})


class TopSecretApiTests(TestCase):
    """Test the top secret API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_coordinates_and_message(self):
        """"Test retrieving coordinates and message"""
        payload = {
            'satellites': [
                {
                    "name": "kenobi",
                    "distance": 485.7,
                    "message": ["este", "", "", "mensaje", ""]
                },
                {
                    "name": "skywalker",
                    "distance": 266.1,
                    "message": ["", "es", "", "", "secreto"]
                },
                {
                    "name": "sato",
                    "distance": 600.5,
                    "message": ["este", "", "un", "", ""]
                }
            ]
        }
        output = {
            'position': {
                'x': -100.0,
                'y': 75.5
            },
            'message': 'este es un mensaje secreto'
        }
        res = self.client.post(TOPSECRET_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, output)

    def test_distances_not_correspond_to_coordinate(self):
        """"Test error recieve when distances no correspond to a valid point"""
        payload = {
            'satellites': [
                {
                    "name": "kenobi",
                    "distance": 485.7,
                    "message": ["este", "", "", "mensaje", ""]
                },
                {
                    "name": "skywalker",
                    "distance": 266.1,
                    "message": ["", "es", "", "", "secreto"]
                },
                {
                    "name": "sato",
                    "distance": 600,
                    "message": ["este", "", "un", "", ""]
                }
            ]
        }
        res = self.client.post(TOPSECRET_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, 'The distances not correspond to a valid coordinate.')

    def test_one_message_is_empty(self):
        """"Test error recieve when a message is missing"""
        payload = {
            'satellites': [
                {
                    "name": "kenobi",
                    "distance": 485.7,
                    "message": ["este", "", "", "mensaje", ""]
                },
                {
                    "name": "skywalker",
                    "distance": 266.1,
                    "message": ["", "es", "", "", "secreto"]
                },
                {
                    "name": "sato",
                    "distance": 600.5,
                    "message": []
                }
            ]
        }
        res = self.client.post(TOPSECRET_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, "The message cant be display because the all the messages aren't the same.")

    def test_one_message_is_missing(self):
        """"Test error recieve when a message is missing"""
        payload = {
            'satellites': [
                {
                    "name": "kenobi",
                    "distance": 485.7,
                    "message": ["este", "", "", "mensaje", ""]
                },
                {
                    "name": "skywalker",
                    "distance": 266.1,
                    "message": ["", "es", "", "", "secreto"]
                },
                {
                    "name": "sato",
                    "distance": 600.5,
                    "message": None
                }
            ]
        }
        res = self.client.post(TOPSECRET_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(
            res.data,
            {'satellites': {2: {'message': [ErrorDetail(string='This field may not be null.', code='null')]}}}
        )

    def test_missing_one_satellite_data(self):
        """Test error when all data from one satellite is missing"""
        payload = {
            'satellites': [
                {
                    "name": "kenobi",
                    "distance": 485.7,
                    "message": ["este", "", "", "mensaje", ""]
                },
                {
                    "name": "skywalker",
                    "distance": 266.1,
                    "message": ["", "es", "", "", "secreto"]
                }
            ]
        }
        res = self.client.post(TOPSECRET_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(
            res.data,
            {'satellites': [ErrorDetail(string='Ensure this field has at least 3 elements.', code='min_length')]}
        )


class TopSecretSplitApiTests(TestCase):
    """Test the top secret split API"""

    def setUp(self):
        self.client = APIClient()

    def test_post_msg_and_distance(self):
        """"Test save coordinates and message"""
        payload = {
            "distance": 485.7,
            "message": ["este", "", "", "mensaje", ""]
        }
        output = [{
            'name': 'kenobi',
            'distance': 485.7,
            'message': ["este", "", "", "mensaje", ""]
        }]
        res = self.client.post(TOPSECRET_SPLIT_KENOBI_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, output)
