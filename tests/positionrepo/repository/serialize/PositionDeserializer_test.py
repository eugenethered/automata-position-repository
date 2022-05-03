import unittest

from core.number.BigFloat import BigFloat

from positionrepo.repository.serialize.position_deserializer import deserialize


class PositionDeserializerTestCase(unittest.TestCase):

    def test_should_deserialize_position(self):
        serialized_position = {
            'instrument': 'OTC',
            'quantity': '1001.01',
            'instant': 1
        }
        position = deserialize(serialized_position)
        self.assertEqual(position.instrument, 'OTC')
        self.assertEqual(position.quantity, BigFloat('1001.01'))
        self.assertEqual(position.instant, 1)
        self.assertIsNone(position.exchanged_from)

    def test_should_deserialize_position_with_exchanged_from(self):
        serialized_position = {
            'instrument': 'OTC',
            'quantity': '1001.01',
            'instant': 1,
            'exchanged_from': 'GBP',
        }
        position = deserialize(serialized_position)
        self.assertEqual(position.instrument, 'OTC')
        self.assertEqual(position.quantity, BigFloat('1001.01'))
        self.assertEqual(position.instant, 1)
        self.assertEqual(position.exchanged_from, 'GBP')


if __name__ == '__main__':
    unittest.main()
