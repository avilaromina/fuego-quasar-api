from django.test import TestCase

from transmission.helpers import (
    get_location,
    get_message,
)


class get_locationTests(TestCase):
    """Test the get_location method"""

    def test_get_location(self):
        """Test that the correct location is calculated"""
        coord = get_location({'kenobi': 485.7, 'skywalker': 266.1, 'sato': 600.5})

        self.assertEqual(coord[0], -100.0)
        self.assertEqual(coord[1], 75.5)

    def test_cant_get_location_missing_distance(self):
        """Test that the location cant be calculated because a distance is missing"""
        self.assertRaises(TypeError, get_location({'kenobi': 485.7, 'skywalker': 266.1, 'sato': None}))

    def test_cant_get_location_invalid_distance(self):
        """Test that the location cant be calculated because a distance has a wrong type"""
        self.assertRaises(TypeError, get_location({'kenobi': 485.7, 'skywalker': 266.1, 'sato': 'Text'}))

    def test_cant_get_location_invalid_distances(self):
        """Test that the location is not return because distances do not correspond to a valid coordinate"""
        coord = get_location({'kenobi': 485.7, 'skywalker': 266.1, 'sato': 600})
        self.assertIsNone(coord)


class get_messageTests(TestCase):
    """Test the get_message method"""

    def test_get_message(self):
        """Test that the correct message is display"""
        msg = get_message([["", "", "!"], ["", "mundo", ""], ["Hola", "", "!"]])
        self.assertEqual(msg, "Hola mundo !")

    def test_incomplete_message(self):
        """Test that the message cant be display because is incomplete"""
        self.assertRaises(TypeError, get_message([["", "", "!"], ["", "mundo", ""], None]))

    def test_empty_message(self):
        """Test that the message cant be display because is incomplete"""
        msg = get_message([["", "", "!"], ["", "mundo", ""], []])
        self.assertIsNone(msg)

    def test_message_not_match(self):
        """Test that the message cant be display because a missmatch"""
        msg = get_message([["", "", "!"], ["", "mundo", ""], ["Hola", "", "chau"]])
        self.assertIsNone(msg)

    def test_get_message_with_delay(self):
        """Test that the correct message is display"""
        msg = get_message([["", "", "!"], ["", "mundo", ""], ["", "", "", "", "Hola", "", "!"]])
        self.assertEqual(msg, "Hola mundo !")
