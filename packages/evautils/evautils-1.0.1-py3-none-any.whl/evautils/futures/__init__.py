from queue import Queue
from typing import Any, List, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed


def multi_thread_executor(execution_threads: int, items: List, func: Callable[[str, List, Any], None], update: Callable[[], None], *args, **kwargs) -> None:
    with ThreadPoolExecutor(max_workers=execution_threads) as executor:
        futures = []
        queue = create_queue(items)
        queue_per_future = max(len(items) // execution_threads, 1)
        while not queue.empty():
            future = executor.submit(func, pick_queue(
                queue, queue_per_future), update, *args, **kwargs)
            futures.append(future)
        for future in as_completed(futures):
            future.result()


def create_queue(items: List) -> Queue:
    queue = Queue()
    for item in items:
        queue.put(item)
    return queue


def pick_queue(queue: Queue, queue_per_future: int) -> List[str]:
    queues = []
    for _ in range(queue_per_future):
        if not queue.empty():
            queues.append(queue.get())
    return queues
