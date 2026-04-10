---
title: "How I Solved LeetCode 2532 with 4 Heaps and an OO Simulation"
date: "2026-04-10"
tags: ["Algorithms", "LeetCode", "Simulation", "Heaps", "Python"]
slug: "lc-2532-bridge-simulation-4-heaps"
summary: "A practical walkthrough of LeetCode 2532 using four priority queues, event-driven time jumps, and a Worker dataclass model that makes a hard simulation problem understandable."
---

# How I Solved LeetCode 2532 with 4 Heaps and an OO Simulation

LeetCode 2532 (Time to Cross a Bridge) looks intimidating at first, but the problem becomes manageable once you model it as a queue-driven simulation.

The key insight is that this is not a graph problem and not a DP problem. It is an **event simulation** problem with strict priority rules.

## Problem in Plain English

- There are `n` boxes on the right side.
- Workers start on the left side.
- Only one worker can be on the bridge at a time.
- Right-to-left crossing has higher priority than left-to-right crossing.
- On each side, choose the least efficient worker first:
  - `inefficiency = left_to_right + right_to_left`
  - if tied, larger index first.

Return the time when the **last box reaches the left side**.

## The 4-Heap Model

I use four heaps to represent worker state:

1. `left_side_worker_ready_q` (max heap): workers waiting on left to cross.
2. `right_side_worker_ready_q` (max heap): workers waiting on right to cross back with a box.
3. `right_side_workers_picking` (min heap): workers currently picking a box on right.
4. `left_side_workers_dropping` (min heap): workers currently dropping a box on left.

This maps directly to the worker lifecycle:

`left_ready -> cross L->R -> right_picking -> right_ready -> cross R->L -> left_dropping -> left_ready`

## Why Event-Driven Time Jump Matters

Sometimes no worker is currently ready to cross, but some are still busy picking or dropping.  
In that case, the bridge is idle and we should jump clock to the next finish event:

```python
clock = min(
    left_side_workers_dropping.peek()[0] if left_side_workers_dropping else float("inf"),
    right_side_workers_picking.peek()[0] if right_side_workers_picking else float("inf"),
)
```

Without this jump, simulation can stall or become inefficient.

## OO Layer That Improved Readability

I used a frozen dataclass for worker timing semantics:

```python
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
```

This keeps queue logic focused on orchestration and keeps time math inside the worker model.

## Core Simulation Order

At each iteration:

1. Release workers whose side work finished at current time.
2. If right-ready exists, cross right-to-left first.
3. Else if left-ready exists and boxes remain to assign, cross left-to-right.
4. Else jump time to next busy-finish event.

This matches problem rules exactly and avoids priority bugs.

## Complexity

- Time: `O((n + k) log k)`
- Space: `O(k)`

## Final Note

The biggest breakthrough for me was treating this as a **state machine + event queue** instead of trying to reason about all workers at once.  
Once the four queues are clear, the rest of the problem becomes mechanical and reliable.
