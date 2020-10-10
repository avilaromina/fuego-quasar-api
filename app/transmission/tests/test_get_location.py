from django.test import TestCase

from transmission.helpers import getLocation


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
        """Test that the location is not return because the tree distances are invalid"""
        coord = getLocation([485.7, 266.1, 600])
        self.assertIsNone(coord)
