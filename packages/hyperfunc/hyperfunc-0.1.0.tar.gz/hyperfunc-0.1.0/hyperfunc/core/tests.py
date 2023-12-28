import pickle

from hyperfunc.core.mq import TaskQueue

task_queue = TaskQueue(host="localhost", port=6379, db="9")

task_queue.lput(pickle.dumps({"a": 1}))
print(task_queue.get())
