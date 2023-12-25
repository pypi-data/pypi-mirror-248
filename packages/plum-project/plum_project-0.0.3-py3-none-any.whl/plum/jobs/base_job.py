import logging
from abc import ABCMeta, abstractmethod
from typing import Optional
from datetime import datetime

class BaseJob(metaclass = ABCMeta):

    def __init__(
        self,
        name: str,
        logger: logging.Logger
    ):
        self._logger: logging.Logger = logger
        self.name: str = name

        self._start_timestamp: Optional[datetime] = None
        self._end_timestamp: Optional[datetime] = None
    
    def _job_execution_time(self) -> Optional[datetime]:
        """Results of None means the job is not complete yet."""
        if self._end_timestamp == None:
            return None
        return (self._end_timestamp - self._end_timestamp)

    @abstractmethod
    def _process(self) -> Optional[Exception]:
        pass
    
    def execute(self):
        self._start_timestamp = datetime.utcnow()
        process_err: Exception = self._process()
        if process_err != None:
            self._logger.error(f'failed to complete the execution of the job "{self.name}"; {process_err.args}')
        self._end_timestamp = datetime.utcnow()
        self._logger.debug(f'job executed in {self._job_execution_time()}')