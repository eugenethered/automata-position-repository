import logging
import unittest

from cache.holder.RedisCacheHolder import RedisCacheHolder
from cache.provider.RedisCacheProviderWithHash import RedisCacheProviderWithHash
from core.number.BigFloat import BigFloat
from core.position.Position import Position

from positionrepo.repository.PositionRepository import PositionRepository


class PositionRepositoryTestCase(unittest.TestCase):

    def setUp(self) -> None:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger('PositionRepository').setLevel(logging.DEBUG)

        options = {
            'REDIS_SERVER_ADDRESS': '192.168.1.90',
            'REDIS_SERVER_PORT': 6379,
            'POSITION_KEY': 'test:position',
            'POSITION_HISTORY_LIMIT': 2
        }
        self.cache = RedisCacheHolder(options, held_type=RedisCacheProviderWithHash)
        self.repository = PositionRepository(options)

    def tearDown(self):
        self.cache.delete('test:position')
        self.cache.delete('test:position:mv:history')

    def test_should_store_and_retrieve_position(self):
        position = Position('OTC', BigFloat('100.00'), 1)
        self.repository.store(position)
        stored_position = self.repository.retrieve()
        self.assertEqual(position, stored_position)

    def test_should_store_position_trade_on_historic_positions_list(self):
        historic_positions = self.repository.retrieve_historic_positions()
        self.assertTrue(len(historic_positions) == 0)
        position = Position('OTC', BigFloat('100.00'), 1, 'BTC')
        self.repository.store(position)
        historic_positions = self.repository.retrieve_historic_positions()
        self.assertTrue(len(historic_positions) == 1)

    def test_should_not_store_position_without_exchanged_from_on_historic_positions_list(self):
        historic_positions = self.repository.retrieve_historic_positions()
        self.assertTrue(len(historic_positions) == 0)
        position = Position('OTC', BigFloat('100.00'), 1)
        self.repository.store(position)
        historic_positions = self.repository.retrieve_historic_positions()
        self.assertTrue(len(historic_positions) == 0)

    def test_should_store_limited_positions_on_historic_positions_list(self):
        historic_positions = self.repository.retrieve_historic_positions()
        self.assertTrue(len(historic_positions) == 0)
        position = Position('OTC', BigFloat('100.00'), 1, 'BTC')
        self.repository.store(position)
        position.instant = 2
        self.repository.store(position)
        position.instant = 3
        self.repository.store(position)
        historic_positions = self.repository.retrieve_historic_positions()
        self.assertEqual(len(historic_positions), 2)

    def test_should_not_receive_a_position_when_there_is_non_present(self):
        position = self.repository.retrieve()
        self.assertIsNone(position)


if __name__ == '__main__':
    unittest.main()
