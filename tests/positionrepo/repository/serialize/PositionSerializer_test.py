import unittest

from core.number.BigFloat import BigFloat
from core.position.Position import Position


class PositionSerializerTestCase(unittest.TestCase):

    def test_should_serialize_position(self):
        position = Position('OTC', BigFloat('1001.01'), 1)
        self.assertEqual(position.instrument, 'OTC')
        self.assertEqual(position.quantity, '1001.01')
        self.assertEqual(position.instant, 1)
        self.assertIsNone(position.exchanged_from)

    def test_should_serialize_position_with_exchanged_from(self):
        position = Position('OTC', BigFloat('1001.01'), 1, 'GBP')
        self.assertEqual(position.instrument, 'OTC')
        self.assertEqual(position.quantity, '1001.01')
        self.assertEqual(position.instant, 1)
        self.assertEqual(position.exchanged_from, 'GBP')


if __name__ == '__main__':
    unittest.main()
