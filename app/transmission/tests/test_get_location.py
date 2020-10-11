from django.test import TestCase

from transmission.helpers import (
    getLocation,
    getMessage,
)


class GetLocationTests(TestCase):
    """Test the GetLocation method"""

    def test_get_location(self):
        """Test that the correct location is calculated"""
        coord = getLocation([485.7, 266.1, 600.5])

        self.assertEqual(coord[0], -100.0)
        self.assertEqual(coord[1], 75.5)

    def test_cant_get_location_missing_distance(self):
        """Test that the location cant be calculated because a distance is missing"""
        self.assertRaises(TypeError, getLocation([485.7, 266.1, None]))

    def test_cant_get_location_invalid_distance(self):
        """Test that the location cant be calculated because a distance has a wrong type"""
        self.assertRaises(TypeError, getLocation([485.7, 266.1, 'Text']))

    def test_cant_get_location_invalid_distances(self):
        """Test that the location is not return because distances do not correspond to a valid coordinate"""
        coord = getLocation([485.7, 266.1, 600])
        self.assertIsNone(coord)


class GetMessageTests(TestCase):
    """Test the GetMessage method"""

    def test_get_message(self):
        """Test that the correct message is display"""
        msg = getMessage([["", "", "!"], ["", "mundo", ""], ["Hola", "", "!"]])
        self.assertEqual(msg, "Hola mundo !")

    def test_incomplete_message(self):
        """Test that the message cant be display because is incomplete"""
        self.assertRaises(TypeError, getMessage([["", "", "!"], ["", "mundo", ""], None]))

    def test_message_not_match(self):
        """Test that the message cant be display because a missmatch"""
        msg = getMessage([["", "", "!"], ["", "mundo", ""], ["Hola", "", "chau"]])
        self.assertIsNone(msg)

    def test_get_message_with_delay(self):
        """Test that the correct message is display"""
        msg = getMessage([["", "", "!"], ["", "mundo", ""], ["", "Hola", "", "!"]])
        self.assertEqual(msg, "Hola mundo !")
