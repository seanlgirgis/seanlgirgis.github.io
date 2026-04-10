"""
LeetCode 2532 - Time to Cross a Bridge (Hard)

Practice scaffold (empty implementation).

What the input means:
- n: number of boxes to move from right -> left
- k: number of workers
- time[i] for worker i is:
  [left_to_right, pick_old_box, right_to_left, put_new_box]

Bridge rules:
1) At most one worker can be on the bridge at any time.
2) Workers waiting on the RIGHT side have higher priority than workers waiting
   on the LEFT side.
3) On the same side, the "less efficient" worker crosses first, where:
   efficiency_key(i) = time[i][0] + time[i][2]
   larger key means less efficient; tie breaks by larger index.

Return:
- Elapsed time when the LAST box reaches the left side.
  (Do not wait for the final put_new_box action.)
"""

import heapq
from dataclasses import dataclass
from typing import Callable, List, Tuple


# --- TEST CASES ---
# Format: (n, k, time_matrix, expected)
tests: List[Tuple[int, int, List[List[int]], int]] = [
    (1, 3, [[1, 1, 2, 1], [1, 1, 3, 1], [1, 1, 4, 1]], 6),
    (3, 2, [[1, 9, 1, 8], [10, 10, 10, 10]], 50),
    (1, 1, [[5, 5, 5, 5]], 15),
    (5, 1, [[1, 1, 1, 1]], 19),
    (10, 5, [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4], [5, 5, 5, 5]], 87),
    (2, 2, [[1, 1, 1, 1], [1, 1, 1, 1]], 4),
    (3, 4, [[1, 2, 3, 4], [4, 3, 2, 1], [1, 1, 1, 1], [10, 10, 10, 10]], 32),
    (2, 3, [[3, 1, 1, 1], [1, 1, 3, 1], [2, 1, 2, 1]], 8),
]


def harness(func: Callable[[int, int, List[List[int]]], int]) -> None:
    """Simple harness for local practice."""
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0

    for test_no, (n, k, time_matrix, expected) in enumerate(tests, 1):
        try:
            got = func(n, k, [row[:] for row in time_matrix])  # defensive copy
            if got == expected:
                print(f"Test {test_no}: PASSED")
                passed += 1
            else:
                short_time = str(time_matrix) if len(time_matrix) <= 3 else f"{time_matrix[:2]}..."
                print(
                    f"Test {test_no}: FAILED | expected={expected}, got={got} "
                    f"| n={n}, k={k}, time={short_time}"
                )
        except Exception as exc:
            short_time = str(time_matrix) if len(time_matrix) <= 3 else f"{time_matrix[:2]}..."
            print(
                f"Test {test_no}: ERROR  | {type(exc).__name__}: {exc} "
                f"| n={n}, k={k}, time={short_time}"
            )

    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


class MaxHeapt:
    def __init__(self) -> None:
        self._data = []

    def push(self, a: int, b: int) -> None:
        heapq.heappush(self._data, (-a, -b))

    def pop(self) -> Tuple[int, int]:
        a, b = heapq.heappop(self._data)
        return -a, -b

    def peek(self) -> Tuple[int, int]:
        a, b = self._data[0]
        return -a, -b

    def __bool__(self) -> bool:
        return bool(self._data)

    def __len__(self) -> int:
        return len(self._data)


class MinHeapt:
    def __init__(self) -> None:
        self._data = []

    def push(self, a: int, b: int) -> None:
        heapq.heappush(self._data, (a, b))

    def pop(self) -> Tuple[int, int]:
        return heapq.heappop(self._data)

    def peek(self) -> Tuple[int, int]:
        return self._data[0]

    def __bool__(self) -> bool:
        return bool(self._data)

    def __len__(self) -> int:
        return len(self._data)

def findCrossingTime_oo(n: int, k: int, time: List[List[int]]) -> int:
    @dataclass(frozen=True)
    class Worker:
        worker_id: int
        left_to_right: int
        pick_box: int
        right_to_left: int
        put_box: int

        @property
        def inefficiency(self) -> int:
            return self.left_to_right + self.right_to_left

        def finish_pick_at_right(self, now: int) -> int:
            return now + self.pick_box

        def finish_put_at_left(self, now: int) -> int:
            return now + self.put_box

    assert k == len(time)
    workers = [
        Worker(
            worker_id=i,
            left_to_right=row[0],
            pick_box=row[1],
            right_to_left=row[2],
            put_box=row[3],
        )
        for i, row in enumerate(time)
    ]
    
    
    boxes_crossed_to_left, clock = 0, 0
    boxes_left_to_assign = n

    # Workers currently waiting on each side to use the bridge.
    left_side_worker_ready_q = MaxHeapt()
    right_side_worker_ready_q = MaxHeapt()

    # Workers currently busy doing non-bridge work.
    left_side_workers_dropping = MinHeapt()   # (finish_time, worker_id)
    right_side_workers_picking = MinHeapt()   # (finish_time, worker_id)

    # Initially, all workers queue on the left_side ready q
    for worker in workers:
        left_side_worker_ready_q.push(worker.inefficiency, worker.worker_id)

    def release_finished_workers(now: int) -> None:
        # Finished dropping on left -> ready on left bridge queue.
        while left_side_workers_dropping and left_side_workers_dropping.peek()[0] <= now:
            _, worker_id = left_side_workers_dropping.pop()
            left_side_worker_ready_q.push(workers[worker_id].inefficiency, worker_id)

        # Finished picking on right -> ready on right bridge queue.
        while right_side_workers_picking and right_side_workers_picking.peek()[0] <= now:
            _, worker_id = right_side_workers_picking.pop()
            right_side_worker_ready_q.push(workers[worker_id].inefficiency, worker_id)
    
    while boxes_crossed_to_left < n:
        # First, release workers who completed side work at current clock.
        release_finished_workers(clock)

        # Priority 1: if any worker on RIGHT is ready, cross back with box.
        if right_side_worker_ready_q:
            _, worker_id = right_side_worker_ready_q.pop()
            worker = workers[worker_id]
            clock += worker.right_to_left
            boxes_crossed_to_left += 1
            if boxes_crossed_to_left == n:
                return clock
            left_side_workers_dropping.push(worker.finish_put_at_left(clock), worker_id)
            continue

        # Priority 2: otherwise, send next LEFT worker to pick a box if any remain.
        if boxes_left_to_assign > 0 and left_side_worker_ready_q:
            _, worker_id = left_side_worker_ready_q.pop()
            worker = workers[worker_id]
            clock += worker.left_to_right
            boxes_left_to_assign -= 1
            right_side_workers_picking.push(worker.finish_pick_at_right(clock), worker_id)
            continue

        # Nobody can cross now -> jump to the earliest side-work finish event.
        next_event_time = min(
            left_side_workers_dropping.peek()[0] if left_side_workers_dropping else float("inf"),
            right_side_workers_picking.peek()[0] if right_side_workers_picking else float("inf"),
        )
        clock = next_event_time

    return clock


def findCrossingTime(n: int, k: int, time: List[List[int]]) -> int:
    """Canonical entrypoint (same logic as OO solution)."""
    return findCrossingTime_oo(n, k, time)


# Complexity (for interview recall):
# Let n = number of boxes, k = number of workers.
# Time: O((n + k) log k)
# Space: O(k)
harness(findCrossingTime_oo)
