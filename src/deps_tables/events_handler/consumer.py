import logging

from deps_message_flow.events.subscriber import (
    DomainEventDispatcher,
    DomainEventHandlersBuilder,
)
from deps_message_flow.messaging.consumer import IMessageConsumer

from deps_tables.constants import PARSED_DATA_AGGREGATE, QUEUE
from deps_tables.domain.events import OCRCompleted

_logger = logging.getLogger(__name__)


def make_consumer(subscriber: IMessageConsumer) -> IMessageConsumer:
    from deps_tables.events_handler.handlers import (  # noqa: WPS433
        ocr_completed_handler,
    )

    _logger.info("Start consuming...")

    events_handlers = (
        DomainEventHandlersBuilder.for_aggregate_type(PARSED_DATA_AGGREGATE)
        .on_event(OCRCompleted, ocr_completed_handler)
        .for_queue(QUEUE)
        .build()
    )

    ded = DomainEventDispatcher(events_handlers, subscriber)
    ded.initialize()

    return subscriber
