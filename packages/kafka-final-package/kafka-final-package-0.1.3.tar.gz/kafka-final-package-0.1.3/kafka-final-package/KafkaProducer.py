import asyncio
from confluent_kafka import Producer, KafkaException
import logging


class KafkaAsyncProducer(Producer):

    def __init__(self, **config):
        super(KafkaAsyncProducer, self).__init__(config)

    @staticmethod
    async def _delivery_report(err, msg):
        if err is not None:
            logging.error(f'Message delivery failed: {err}')
        else:
            logging.info(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

    async def send_message_async(self, topic, key, value, callback=None):
        try:
            self.produce(
                topic,
                key=key,
                value=value,
                callback=lambda err, msg: asyncio.ensure_future(self._delivery_report(err, msg))
            )
            await asyncio.sleep(0)
        except KafkaException as e:
            logging.error(f'Error sending message asynchronously: {e}')
        finally:
            self.flush()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.flush()


class KafkaSyncProducer(Producer):

    def __init__(self, **config):
        super(KafkaSyncProducer, self).__init__(config)

    @staticmethod
    def _delivery_report(err, msg):
        if err is not None:
            logging.error(f'Message delivery failed: {err}')
        else:
            logging.info(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

    def send_message_sync(self, topic, key, value):
        try:
            self.produce(
                topic,
                key=key,
                value=value,
                callback=self._delivery_report
            )
            self.flush()
        except KafkaException as e:
            logging.error(f'Error sending message synchronously: {e}')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.flush()