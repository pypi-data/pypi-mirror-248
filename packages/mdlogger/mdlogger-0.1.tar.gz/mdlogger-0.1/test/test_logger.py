import pytest
import os

from mdlogger import logger

basepath = os.path.abspath('.')
log_path = os.path.abspath(os.path.join(basepath, 'logs'))
error_path = os.path.join(log_path, 'errors')


def test_create_log_folder():

    assert os.path.exists(log_path)
    assert os.path.exists(error_path)


def test_log_message_in_correct_file():
    logger.info('info log')
    logger.error('error message')
    full_log = os.path.join(log_path, 'full.log.md')
    current = os.path.join(log_path, 'current.run.log.md')
    error = os.path.join(log_path, 'errors/error.log.md')

    assert os.path.exists(full_log)
    assert os.path.exists(current)

    with open(full_log, 'r') as f:
        log = '\n'.join(f.readlines())
        assert log.index('info log') > 0

    with open(current, 'r') as f:
        log = '\n'.join(f.readlines())
        assert log.index('info log') > 0

    with open(error, 'r') as f:
        log = '\n'.join(f.readlines())
        assert log.index('error message') > 0
