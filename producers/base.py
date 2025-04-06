from abc import ABC, abstractmethod

class Poller(ABC):

    def __init__(self, end_point, producer=None):
        self.producer = producer
        self.end_point = end_point

    @abstractmethod
    def poll(self):
        pass

    @abstractmethod
    def publish(self):
        pass



class EventTransformer(ABC):
    def __init__(self, event):
        self.event = event

    @abstractmethod
    def transform(self):
        pass


class KafkaTopic(ABC):
    def __init__(self, topic_name, topic_type=None):
        self.topic_name = topic_name
        self.topic_type = topic_type
        
    @abstractmethod
    def produce(self, event, topic_name):
        pass
