from django.test import TestCase

from transmission.helpers import (
    get_location,
    get_message,
)


class get_locationTests(TestCase):
    """Test the get_location method"""

    def test_get_location(self):
        """Test correct location"""
        coord = get_location({'kenobi': 485.41, 'skywalker': 265.75, 'sato': 600.52})

        self.assertEqual(coord[0], -100)
        self.assertEqual(coord[1], 75)

    def test_cant_get_location_missing_distance(self):
        """Test missing distance"""
        self.assertRaises(TypeError, get_location({'kenobi': 485.7, 'skywalker': 266.1, 'sato': None}))

    def test_cant_get_location_invalid_distance(self):
        """Test mistype distance"""
        self.assertRaises(TypeError, get_location({'kenobi': 485.7, 'skywalker': 266.1, 'sato': 'Text'}))

    def test_cant_get_location_invalid_distances(self):
        """Test invalid coordinate"""
        coord = get_location({'kenobi': 485.7, 'skywalker': 266.1, 'sato': 600})
        self.assertIsNone(coord)


class get_messageTests(TestCase):
    """Test get_message method"""

    def test_get_message(self):
        """Test correct message"""
        msg = get_message([["", "", "!"], ["", "mundo", ""], ["Hola", "", "!"]])
        self.assertEqual(msg, "Hola mundo !")

    def test_incomplete_message(self):
        """Test incomplete message"""
        self.assertRaises(TypeError, get_message([["", "", "!"], ["", "mundo", ""], None]))

    def test_empty_message(self):
        """Test invalid message"""
        msg = get_message([["", "", "!"], ["", "mundo", ""], []])
        self.assertIsNone(msg)

    def test_message_not_match(self):
        """Test mismatch message"""
        msg = get_message([["", "", "!"], ["", "mundo", ""], ["Hola", "", "chau"]])
        self.assertIsNone(msg)

    def test_get_message_with_delay(self):
        """Test message delay"""
        msg = get_message([["", "", "!"], ["", "mundo", ""], ["", "", "", "", "Hola", "", "!"]])
        self.assertEqual(msg, "Hola mundo !")
