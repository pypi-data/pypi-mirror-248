'''
Wrapper for the module logging, aimed for simple scripts.

Logs can be printed using:
 * logd - a function for debug message.
 * logi - a function for info message.
 * loge - a function for error message.
 * logt - a decorator applied to functions, prints logs on enter and return.

logc is a configuration function, see its description for the details.
'''

__all__ = [
    'logc',
    'logt',
    'logd',
    'logi',
    'loge',
]


import logging
import os
import sys
import threading
import traceback
from datetime import datetime
from inspect import getmodule
from typing import Callable


#
# Implementation.
#


LOGGER = logging.getLogger()
HANDLER = logging.StreamHandler()
FORMATTER = logging.Formatter('%(message)s')
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)

CONFIG_VERBOSE = False
CONFIG_DETAILED = True


class Level:
    '''
    Represents log level.

    Fields:
     * name - a single letter that denotes the level.
     * log  - a function from the logging module to print a message.
    '''

    def __init__(
        self,
        name: 'str',
        log: 'Callable[[str], None]',
    ) -> 'None':
        self.name = name
        self.log = log


# Actual levels. Note that trace and debug use the same function.
LEVEL_T = Level('T', logging.debug)
LEVEL_D = Level('D', logging.debug)
LEVEL_I = Level('I', logging.info)
LEVEL_E = Level('E', logging.error)


def log_ts() -> 'str':
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')


def log_pid() -> 'str':
    return f'{os.getpid():>7}'


TID = {os.getpid(): os.getpid()}


def log_tid() -> 'str':
    if sys.version_info.minor > 7:
        # Use the real id.
        id_os = threading.get_native_id()
    else:
        # Generate a fake id, but still a unique one.
        id_py = threading.get_ident()
        id_os = TID.get(id_py, os.getpid() + len(TID))
        if id_py not in TID:
            TID[id_py] = id_os
    return f'{id_os:<7}'


def log_path() -> 'str':
    entry = traceback.extract_stack()[-5]
    return f'{os.path.basename(entry.filename)}:{entry.name}'


def log_prefix(name) -> 'str':
    return f'{log_ts()} {log_pid()} {log_tid()} [{name}] {log_path()}: '


def log(
    level: 'Level',
    message: 'object',
) -> 'None':
    '''
    Encapsulates message printing.
    '''
    if isinstance(message, BaseException) and CONFIG_VERBOSE:
        message = ''.join(traceback.format_exception(
            type(message), message, message.__traceback__))[:-1]
    else:
        message = str(message)
    prefix = log_prefix(level.name) if CONFIG_DETAILED else ''
    for x in message.split('\n'):
        level.log(prefix + x)


#
# Interface.
#


def logt(func):
    '''
    Decorator, when applied to functions, prints trace messages ('T'):
     * Enter FILE:FUNCTION after function is called.
     * Leave FILE:FUNCTION after return.
    '''
    file = os.path.basename(getmodule(func).__file__)

    def wrapper(*args, **kwargs):
        log(LEVEL_T, f'Enter {file}:{func.__qualname__}.')
        ret = func(*args, **kwargs)
        log(LEVEL_T, f'Leave {file}:{func.__qualname__}.')
        return ret
    return wrapper


def logd(message: 'object') -> 'None':
    '''
    Print debug message ('D').

    Parameters:
     * message - can be anything, will be converted to string.

    Return:
     * None.
    '''
    log(LEVEL_D, message)


def logi(message: 'object') -> 'None':
    '''
    Print info message ('I').

    Parameters:
     * message - can be anything, will be converted to string.

    Return:
     * None.
    '''
    log(LEVEL_I, message)


def loge(message: 'object') -> 'None':
    '''
    Print error message ('E').

    Parameters:
     * message - can be anything, will be converted to string.

    Return:
     * None.
    '''
    log(LEVEL_E, message)


def logc(
    verbose: 'bool' = None,
    detailed: 'bool' = None,
) -> 'None':
    '''
    Function to configure logging. It is called upon import to set the defaults.
    In subsequent calls, if some of the parameters are not set their current
    value is retained.

    Parameters:
     * verbose  - whether to print debug and trace logs.
     * detailed - whether to prefix message with extra information.

    Return:
     * None.
    '''
    global CONFIG_VERBOSE
    if verbose == None:
        verbose = CONFIG_VERBOSE
    CONFIG_VERBOSE = verbose
    LOGGER.setLevel(logging.DEBUG if verbose else logging.INFO)
    global CONFIG_DETAILED
    if detailed == None:
        detailed = CONFIG_DETAILED
    CONFIG_DETAILED = detailed


logc()
