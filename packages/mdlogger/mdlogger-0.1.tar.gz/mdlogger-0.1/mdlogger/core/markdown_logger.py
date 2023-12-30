from typing import Iterable

import os
import logging.config
import logging


class MarkdownLogger:
    """ logging module wrapper class

    Instance will be create when the package is loaded.
    With default settings, log files will be stored in the `project/root/logs` directory.
    separated errors log files will be stored in the `project/root/logs/errors` directory.

    If this is good for you. you can just import the logger and use it as normal logger.

    `from mdlogger import logger`

    Or create a new instance with custom connfig and use the logger property:

    `logger = MarkdownLogger(...).logger`
    """

    logger_name = 'MarkdownLogger'

    def __init__(
            self,
            path='.',
            level=logging.DEBUG,
            console_output=True,
            one_time_log=True,
            sep_error_log=True,
            filters: Iterable = None,
            custom_handlers: Iterable = None
    ):
        """ 

        Args:
            path (str, optional): Log root path. Defaults to '.'.
            level (int, optional): log level, use `logging.DEBUG` or other level you need. Defaults to logging.DEBUG.
            console_output (bool, optional): Console handler with same level with logger level. Defaults to True.
            one_time_log (bool, optional): Write mode FileHandler, refresh log content every time. Defaults to True.
            sep_error_log (bool, optional): separately ERROR level log in `errors` folder under the base log path. Defaults to True.
            filters (Iterable, optional): Filters for this logger. Defaults to None.
            custom_handlers (Iterable, optional): Other handlers. Defaults to None.
        """
        base_path = os.path.abspath(path)
        self._log_path = os.path.abspath(os.path.join(base_path, 'logs'))
        self._error_path = os.path.abspath(
            os.path.join(self._log_path, 'errors'))
        self._create_log_folder()

        self.level = level
        self.custom_handlers = custom_handlers
        self.filters = filters
        self.sep_error_log = sep_error_log
        self.one_time_log = one_time_log
        self.console_output = console_output

    def _create_log_folder(self):
        if not os.path.exists(self._log_path):
            os.mkdir(self._log_path)
            print(f'> Create log folder at: {self._log_path}')

        if not os.path.exists(self._error_path):
            os.mkdir(self._error_path)
            print(f'> Create log folder at: {self._error_path}')

    def _markdown_handler(self):
        handler = logging.handlers.RotatingFileHandler(
            filename=os.path.join(self._log_path, 'full.log.md'),
            mode='a',
            maxBytes=1024*1024,
            backupCount=10,
            encoding='utf-8'
        )
        handler.setFormatter(self._file_formatter())
        handler.level = self.level
        return handler

    def _console_handler(self):
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(self._consolle_formatter())
        return handler

    def _onetime_handler(self):
        handler = logging.FileHandler(
            filename=os.path.join(self._log_path, 'current.run.log.md'),
            mode='w',
            encoding='utf-8'
        )
        handler.setLevel(logging.NOTSET)
        handler.setFormatter(self._file_formatter())
        return handler

    def _error_handler(self):
        handler = logging.handlers.RotatingFileHandler(
            filename=os.path.join(self._error_path, 'error.log.md'),
            mode='a',
            maxBytes=1024*1024,
            backupCount=10,
            encoding='utf-8'
        )
        handler.setFormatter(self._file_formatter())
        handler.level = logging.ERROR
        return handler

    def _consolle_formatter(self):
        fmt = (
            '>> %(levelname)s [%(process)d:%(threadName)s] `%(module)s.%(funcName)s%(args)s` - %(asctime)s:\n'
            '\t%(message)s'
        )
        return logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")

    def _file_formatter(self):
        fmt = (
            '#### '
            '`%(module)s`.`%(funcName)s%(args)s`::`%(filename)s`:`%(lineno)d` - %(asctime)s.%(msecs)03d:\n'
            '**%(levelname)s** [PID:`%(process)d`:THREAD:`%(threadName)s`]\n'
            '```plaintext\n'
            '%(message)s\n'
            '```\n'
            '--------\n'
        )
        return logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")

    @property
    def logger(self):
        self._logger = logging.getLogger(MarkdownLogger.logger_name)
        self._logger.setLevel(self.level)
        self._logger.addHandler(self._markdown_handler())
        if self.one_time_log:
            self._logger.addHandler(self._onetime_handler())
        if self.sep_error_log:
            self._logger.addHandler(self._error_handler())
        if self.console_output:
            self._logger.addHandler(self._console_handler())
        if self.custom_handlers:
            for handler in custom_handlers:
                self._logger.addHandler(handler)
        if self.filters:
            for filter in filters:
                self._logger.addFilter(filter)
        return self._logger
