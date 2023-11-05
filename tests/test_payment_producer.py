import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from app.controllers.producers.payment_processing import send_rider_payment, send_driver_earning

class TestPaymentProducer(unittest.TestCase):
    @patch('app.controllers.producers.payment_processing.producer')
    def test_send_rider_payment(self, mock_producer):
        rider_id = 123
        amount = 45.0
        payment_date = datetime.now()

        send_rider_payment(rider_id, amount, payment_date)
        mock_producer.send.assert_called_once()

class TestEarningProducer(unittest.TestCase):
    @patch('app.controllers.producers.payment_processing.producer')
    def test_send_driver_earning(self, mock_producer):
        driver_id = 123
        amount = 45.0
        payment_date = datetime.now()

        send_driver_earning(driver_id, amount, payment_date)
        mock_producer.send.assert_called_once()


if __name__ == '__main__':
    unittest.main()