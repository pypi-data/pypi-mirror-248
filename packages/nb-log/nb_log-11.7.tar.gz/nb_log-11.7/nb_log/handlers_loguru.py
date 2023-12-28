import logging
import os
import sys
import typing
import uuid
from nb_log import nb_log_config_default


class LoguruStreamHandler(logging.Handler):
    """
    loguru 的 控制台效果
    """

    format = ("<green>{time:YYYY-MMDD HH:mm:ss.SSS}</green> | {extra[namespace]} | "
              "<level>{level: <8}</level> | "
              "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

    def __init__(self, logger_name, sink: typing.Any = sys.stdout):
        logging.Handler.__init__(self)
        self._logger_name = logger_name
        self._sink = sink
        from loguru._logger import Logger, Core

        # print(logger._core.handlers)
        # try:
        #     logger.remove(0)
        # except ValueError as e:
        #     pass
        # print(e)
        logger = Logger(
            core=Core(),
            exception=None,
            depth=6,  # 写6是为了显示实际的日志发生处，而不是封装loguru的emit方法处。
            record=False,
            lazy=False,
            colors=False,
            raw=False,
            capture=True,
            patchers=[],
            extra={},
        )

        self._bind_for = uuid.uuid4()
        self._add_handler(logger, )
        # print(logger._core.handlers)
        self.logurux = logger.bind(namespace=logger_name,
                                   # bind_for = self._bind_for
                                   )
        # options_list = list(self.logurux._options)
        # options_list[1] = 6  # 转化是为了显示实际的日志发生处，而不是封装loguru的emit方法处。
        # self.logurux._options = tuple(options_list)
        # print(logger_name, self.logurux._core.handlers)

    def _add_handler(self, logger, ):
        logger.add(self._sink,
                   # filter=lambda record: record["extra"]["bind_for"] == self._bind_for,
                   format=self.format)
        # logger.add(self._log_to, filter=lambda record: record["extra"]["namespace"] == self._logger_name, format=self.format)

    def emit(self, record):
        # noinspection PyUnresolvedReferences
        level_str = logging._levelToName[record.levelno]
        # self.logurux.log(level_str, self.format(record))
        self.logurux.log(level_str, record.getMessage())


class LoguruFileHandler(LoguruStreamHandler):
    """
    loguru 的 文件日志写入
    """

    def _add_handler(self, logger, ):
        '''

        :param logger:
        :return:
        '''
        log_file_full_path = self._sink
        # rotation = "100 MB"  "00:00"
        arr = log_file_full_path.split('.')
        part1 = '.'.join(arr[:-1])
        part2 = arr[-1]
        loguru_file = f'{part1}.{{time:YYYYMMDD}}.loguru.{part2}'

        # rotation_size = 1024 * 1024  # 1MB
        rotation_size = f"{nb_log_config_default.LOG_FILE_SIZE} MB"
        rotation_time = "00:00"  # 每天的 00:00

        logger.add(loguru_file,
                   # filter=lambda record: record["extra"]["bind_for"] == self._bind_for,
                   format=self.format,
                   enqueue=True,
                   # rotation=f"{nb_log_config_default.LOG_FILE_SIZE} MB",
                   rotation=rotation_time,
                   retention=nb_log_config_default.LOG_FILE_BACKUP_COUNT
                   )
