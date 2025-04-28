from abc import ABC, abstractmethod
from typing import Any, Optional


class Consumer(ABC):
    def __init__(
        self,
        end_point: str,
        consumer: Optional[Any] = None,
        topic_name: Optional[str] = None,
        consumer_group: Optional[str] = None,
    ):
        self.consumer = consumer
        self.end_point = end_point
        self.topic_name = topic_name
        self.consumer_group = consumer_group

    @abstractmethod
    def consume(self) -> None:
        """Consume messages from the source."""
        pass

    @abstractmethod
    def process(self) -> None:
        """Process consumed messages."""
        pass
