from abc import ABC, abstractmethod


class Consumer(ABC):

    def __init__(self, end_point, consumer=None, topic_name=None, consumer_group=None):
        self.consumer = consumer
        self.end_point = end_point
        self.topic_name = topic_name
        self.consumer_group = consumer_group

    @abstractmethod
    def consume(self):
        pass

    @abstractmethod
    def process(self):
        pass
