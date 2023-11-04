import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from app.controllers.producers import payment_processing
from app.controllers.producers.payment_processing import send_rider_payment

class TestKafkaProducer(unittest.TestCase):
    @patch('payment_processing.KafkaProducer')
    def test_send_rider_payment(self, mock_producer):
        # Mock the KafkaProducer instance and its methods
        mock_producer.return_value = Mock()
        payment_topic = 'payment_topic'
        rider_id = 123
        amount = 45.0
        payment_date = datetime.now()

        # Call the producer function that sends a message to Kafka
        send_rider_payment(rider_id, amount, payment_date)

        # Assert the producer method was called with the correct arguments
        mock_producer.return_value.send.assert_called_once_with(payment_topic, {
            "rider_id": rider_id,
            "amount": amount,
            "payment_date": payment_date
        })
        
        mock_producer.return_value.flush.assert_called_once()

if __name__ == '__main__':
    unittest.main()