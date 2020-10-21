from unittest import mock, skip
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient


TOPSECRET_URL = reverse('transmission:topsecret')
TOPSECRET_SPLIT_KENOBI_URL = reverse('transmission:topsecret_split', kwargs={'name': 'kenobi'})
TOPSECRET_SPLIT_PALPATINE_URL = reverse('transmission:topsecret_split', kwargs={'name': 'palpatine'})


class TopSecretApiTests(TestCase):
    """Test topsecret API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_coordinates_and_message(self):
        """"Test retrieve coordinates and message"""
        payload = {
            'satellites': [
                {
                    "name": "kenobi",
                    "distance": 485.41,
                    "message": ["este", "", "", "mensaje", ""]
                },
                {
                    "name": "skywalker",
                    "distance": 265.75,
                    "message": ["", "es", "", "", "secreto"]
                },
                {
                    "name": "sato",
                    "distance": 600.52,
                    "message": ["este", "", "un", "", ""]
                }
            ]
        }
        output = {
            'position': {
                'x': -100.0,
                'y': 75.0
            },
            'message': 'este es un mensaje secreto'
        }
        res = self.client.post(TOPSECRET_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, output)

    def test_distances_not_correspond_to_coordinate(self):
        """"Test invalid distances"""
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
        self.assertEqual(res.data, 'Distances do not match a valid coordinate.')

    def test_one_message_is_empty(self):
        """"Test empty message"""
        payload = {
            'satellites': [
                {
                    "name": "kenobi",
                    "distance": 485.41,
                    "message": ["este", "", "", "mensaje", ""]
                },
                {
                    "name": "skywalker",
                    "distance": 265.75,
                    "message": ["", "es", "", "", "secreto"]
                },
                {
                    "name": "sato",
                    "distance": 600.52,
                    "message": []
                }
            ]
        }
        res = self.client.post(TOPSECRET_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, "Invalid message or format.")

    def test_one_message_is_missing(self):
        """"Test single missing message"""
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
        """Test single satellite missing data"""
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

    def test_satellite_name_is_not_valid(self):
        """"Test invalid satellite name"""
        payload = {
            'satellites': [
                {
                    "name": "palpatine",
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
        res = self.client.post(TOPSECRET_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(
            res.data,
            {
                'satellites': {
                    0: {
                        'name': [ErrorDetail(string='"palpatine" is not a valid choice.', code='invalid_choice')]
                    }
                }
            }
        )

    def test_duplicate_information_for_same_satellite(self):
        """"Test dupliclate satellite names"""
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
                    "name": "kenobi",
                    "distance": 600.5,
                    "message": ["este", "", "un", "", ""]
                }
            ]
        }
        res = self.client.post(TOPSECRET_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, 'Distances do not match a valid coordinate.')


class TopSecretSplitApiTests(TestCase):
    """Test topsecret_split API"""

    def setUp(self):
        self.client = APIClient()

    def test_post_msg_and_distance(self):
        """"Test save distance and message"""
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

    def test_post_invalid_distance(self):
        """"Test invalid distance"""
        payload = {
            "distance": 'distance',
            "message": ["este", "", "", "mensaje", ""]
        }
        res = self.client.post(TOPSECRET_SPLIT_KENOBI_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(res.data, {'distance': [ErrorDetail(string='A valid number is required.', code='invalid')]})

    def test_post_invalid_satellite_name(self):
        """"Test invalid satellite name"""
        payload = {
            "distance": 782.89,
            "message": ["este", "", "", "mensaje", ""]
        }
        res = self.client.post(TOPSECRET_SPLIT_PALPATINE_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, [ErrorDetail(string="palpatine isn't a valid sattelite name", code='invalid')])

    @skip('Serializer can\'t validate message format')
    def test_post_invalid_message(self):
        """"Test invalid distance"""
        payload = {
            "distance": 100,
            "message": ["este", "", "", 1627, ""]
        }
        res = self.client.post(TOPSECRET_SPLIT_KENOBI_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(res.data, {'message': [ErrorDetail(string='Not a valid string.', code='invalid')]})

    def test_get_coordinates_and_message(self):
        """Test retrieve previously loaded message and coordinates"""
        tmp_transmissions = {
            'kenobi': (485.41, ["este", "", "", "mensaje", ""]),
            'skywalker': (265.75, ["", "es", "", "", "secreto"]),
            'sato': (600.52, ["este", "", "un", "", ""]),
        }
        output = {
            'position': {
                'x': -100.0,
                'y': 75.0
            },
            'message': 'este es un mensaje secreto'
        }
        with mock.patch('transmission.helpers.tmp_transmissions', tmp_transmissions):
            res = self.client.get(TOPSECRET_SPLIT_KENOBI_URL)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, output)

    def test_second_get_dont_show_message_and_coordinates(self):
        """Test empty call after retrieving previously loaded messages"""
        tmp_transmissions = {
            'kenobi': (485.41, ["", "este", "", "", "mensaje", ""]),
            'skywalker': (265.75, ["", "", "es", "", "", "secreto"]),
            'sato': (600.52, ["", "este", "", "un", "", ""]),
        }
        with mock.patch('transmission.helpers.tmp_transmissions', tmp_transmissions):
            res = self.client.get(TOPSECRET_SPLIT_KENOBI_URL)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            res2 = self.client.get(TOPSECRET_SPLIT_KENOBI_URL)
            self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(res2.data, 'Distances do not match a valid coordinate.')
