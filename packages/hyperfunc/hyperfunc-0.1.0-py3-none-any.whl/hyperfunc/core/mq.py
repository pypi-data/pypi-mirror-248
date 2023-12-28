import time
from urllib.parse import urlparse

from redis import Redis

from hyperfunc.config import REDIS_URL


class BaseRedisConn:
    def __init__(self, host: str, port: int, db: str):
        self._conn = Redis(host=host, port=port, db=db)


class TaskQueue(BaseRedisConn):
    PENDING_QUEUE = "hyperfunc_pending_queue"  # 待执行队列
    PROCESSING_QUEUE = "hyperfunc_processing_queue"  # 执行中的队列

    def lput(self, message: bytes):
        self._conn.lpush(self.PENDING_QUEUE, message)

    def rput(self, message: bytes):
        # 因为 get 是从右边开始，所以从右边 put 相当于插队，优先执行
        self._conn.rpush(self.PENDING_QUEUE, message)

    def get(self):
        return self._conn.brpoplpush(self.PENDING_QUEUE, self.PROCESSING_QUEUE)

    def ack(self, message: bytes):
        self._conn.lrem(self.PROCESSING_QUEUE, 1, message)  # type: ignore

    def load_processing(self):
        while self._conn.llen(self.PROCESSING_QUEUE) > 0:
            self._conn.rpoplpush(self.PROCESSING_QUEUE, self.PENDING_QUEUE)


class DelayQueue(BaseRedisConn):
    DELAY_QUEUE = "hyperfunc_delay_queue"  # 延迟队列

    def put(self, message: bytes, run_at: float | int):
        self._conn.zadd(self.DELAY_QUEUE, {message: run_at})

    def get(self) -> list[bytes]:
        while 1:
            now = time.time()
            tasks = self._conn.zrangebyscore(self.DELAY_QUEUE, 0, now)
            yield tasks

    def ack(self, messages: list[bytes]):
        for message in messages:
            self._conn.zrem(self.DELAY_QUEUE, message)


parsed_url = urlparse(REDIS_URL)
redis_params = {"host": parsed_url.hostname, "port": parsed_url.port, "db": parsed_url.path.lstrip("/")}

task_queue = TaskQueue(**redis_params)
delay_queue = DelayQueue(**redis_params)
