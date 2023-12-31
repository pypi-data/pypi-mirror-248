import logging
import threading

from google.cloud import spanner

from sparta.spanner import DBService


class DBServiceProvider:
    """
    Provides DBService instances.
    Responsible for creation and re-utilization of existing instances.
    """

    def __init__(
        self,
        instance_id: str,
        pool_size: int = None,
        session_request_timeout: int = None,
    ) -> None:
        super().__init__()
        self.logger = logging.getLogger(f"{__name__}.{type(self).__name__}")
        self.default_instance_id = instance_id
        self.default_pool_size = pool_size
        self.default_session_request_timeout = session_request_timeout
        self._spanner_client = spanner.Client()
        self._instances = {}
        # Use lock to assure thread-safety.
        # See https://medium.com/analytics-vidhya/how-to-create-a-thread-safe-singleton-class-in-python-822e1170a7f6
        self._lock = threading.Lock()

    def get_by_database_id(
        self,
        database_id: str,
        pool_size: int = None,
        session_request_timeout: int = None,
    ) -> DBService:
        if database_id not in self._instances:
            with self._lock:
                # Another thread could have created the instance before we acquired the lock. Double-check.
                if database_id not in self._instances:
                    self._instances[database_id] = DBService(
                        instance_id=self.default_instance_id,
                        database_id=database_id,
                        pool_size=pool_size
                        if pool_size is not None
                        else self.default_pool_size,
                        session_request_timeout=session_request_timeout
                        if session_request_timeout is not None
                        else self.default_session_request_timeout,
                        spanner_client=self._spanner_client,
                    )
        return self._instances[database_id]
