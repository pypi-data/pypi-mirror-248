import logging
import structlog
import ctypes
import pathlib

def add_module_and_lineno(logger: logging.Logger, method_name: str, event_dict: dict):
    try:
        frame, module_str = structlog._frames._find_first_app_frame_and_name(additional_ignores=[__name__, 'logging'])
        event_dict['module'] = module_str
        event_dict['lineno'] = frame.f_lineno
    except:
        pass
    return event_dict

try:
    dir = pathlib.Path(__file__).parent.resolve()
    libc = ctypes.cdll.LoadLibrary(str(dir / "perfomance_logging.pyd"))
    log = libc.Log
    log.argtypes = [ctypes.c_char_p]
except:
    log = lambda x: x

def set_logger():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processors=[
                structlog.stdlib.add_log_level,
                structlog.stdlib.add_logger_name,
                structlog.processors.TimeStamper(fmt='iso'),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.stdlib.PositionalArgumentsFormatter(),
                add_module_and_lineno,
                elastic_format,
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.dev.ConsoleRenderer()
            ]
        )
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(stream_handler)

def elastic_format(logger: logging.Logger, method_name: str, event_dict: dict):
    # Elastic requires the message to be under 'message' and not under 'event'
    try:
        if isinstance(event_dict, dict) and 'event' in event_dict:
            log(event_dict.get('event').encode('utf-8'))
    except:
        pass

    return event_dict
