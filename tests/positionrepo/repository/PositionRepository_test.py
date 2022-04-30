import unittest

from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.number.BigFloat import BigFloat
from core.position.Position import Position

from positionrepo.repository.PositionRepository import PositionRepository


class PositionRepositoryTestCase(unittest.TestCase):

    def setUp(self) -> None:
        options = {
            'REDIS_SERVER_ADDRESS': '192.168.1.90',
            'REDIS_SERVER_PORT': 6379,
            'POSITION_KEY': 'test:position'
        }
        self.cache = RedisCacheHolder(options)
        self.repository = PositionRepository(options)

    def tearDown(self):
        self.cache.delete('test:position')

    def test_should_store_and_retrieve_position(self):
        position = Position('OTC', BigFloat('100.00'), 1)
        self.repository.store(position)
        stored_position = self.repository.retrieve()
        self.assertEqual(position, stored_position)


if __name__ == '__main__':
    unittest.main()
