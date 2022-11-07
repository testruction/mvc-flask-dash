import logging

from opentelemetry.instrumentation.logging import LoggingInstrumentor


def init_logger(args):
    if args.debug:
        LoggingInstrumentor().instrument(log_level=logging.DEBUG,
                                         set_logging_format=True)
    else:
        LoggingInstrumentor().instrument(log_level=logging.INFO,
                                         set_logging_format=True)
