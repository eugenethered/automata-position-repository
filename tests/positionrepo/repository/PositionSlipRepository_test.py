import logging
import unittest

from cache.holder.RedisCacheHolder import RedisCacheHolder
from cache.provider.RedisCacheProviderWithHash import RedisCacheProviderWithHash
from core.number.BigFloat import BigFloat
from core.position.PositionSlip import PositionSlip, Status

from positionrepo.repository.PositionSlipRepository import PositionSlipRepository


class PositionSlipRepositoryTestCase(unittest.TestCase):

    def setUp(self) -> None:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger('ExchangeTransformRepository').setLevel(logging.DEBUG)

        options = {
            'REDIS_SERVER_ADDRESS': '192.168.1.90',
            'REDIS_SERVER_PORT': 6379,
            'POSITION_SLIP_KEY': 'test:position:slip'
        }
        self.cache = RedisCacheHolder(options)
        self.repository = PositionSlipRepository(options)

    def tearDown(self):
        self.cache.delete('test:position:slip')

    def test_should_store_and_retrieve_position_slip(self):
        position_slip = PositionSlip('OTC', BigFloat('100.00'), Status.USED)
        self.repository.store(position_slip)
        stored_position_slip = self.repository.retrieve()
        self.assertEqual(position_slip, stored_position_slip)

    def test_should_not_receive_a_position_slip_when_there_is_non_present(self):
        position_slip = self.repository.retrieve()
        self.assertIsNone(position_slip)


if __name__ == '__main__':
    unittest.main()
