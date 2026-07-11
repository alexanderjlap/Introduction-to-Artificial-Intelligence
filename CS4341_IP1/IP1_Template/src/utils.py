# YOU SHOULD NOT HAVE TO MODIFY THIS FILE
# YOU SHOULD NOT HAVE TO MODIFY THIS FILE
# YOU SHOULD NOT HAVE TO MODIFY THIS FILE

import functools

def memoize(fn, slot=None, maxsize=4096):
    """Memoize fn: make it remember the computed value for any argument list.
    If slot is specified, store result in that slot of first argument.
    If slot is false, use lru_cache for caching the values."""
    if slot:

        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:

        @functools.lru_cache(maxsize=maxsize)
        def memoized_fn(*args):
            return fn(*args)

    return memoized_fn


class PriorityQueue:
    """
    Min-priority queue.

    API:
        q = PriorityQueue()
        q.put(obj, priority)
        obj, priority = q.pop()
        priority = q[obj]
        obj in q
        q.update_priority(obj, new_priority)

    Notes:
    - obj must be hashable
    """

    def __init__(self):
        self._heap = []      # [priority, obj]
        self._index = {}     # obj -> heap index

    # -----------------------------
    # API methods
    # -----------------------------
    def put(self, obj, priority):
        self._check_hashable(obj)

        if obj in self._index:
            raise ValueError(f"{obj!r} already exists in the priority queue, use update_priority to change its priority")

        i = len(self._heap)
        self._heap.append([priority, obj])
        self._index[obj] = i
        self._bubble_up(i)

    def pop(self):
        if not self._heap:
            raise IndexError("Cannot pop from an empty PriorityQueue")

        priority, obj = self._heap[0]
        last = self._heap.pop()
        del self._index[obj]

        if self._heap:
            self._heap[0] = last
            _, moved_obj = last
            self._index[moved_obj] = 0
            self._bubble_down(0)

        return obj, priority

    def update_priority(self, obj, new_priority):
        self._check_hashable(obj)

        if obj not in self._index:
            raise KeyError(f"{obj!r} is not in the priority queue")

        i = self._index[obj]
        old_priority = self._heap[i][0]
        self._heap[i][0] = new_priority

        if new_priority < old_priority:
            self._bubble_up(i)
        elif new_priority > old_priority:
            self._bubble_down(i)

    # -----------------------------
    # basic container interface
    # -----------------------------
    def __len__(self):
        return len(self._heap)

    def __contains__(self, obj):
        self._check_hashable(obj)
        return obj in self._index

    def __getitem__(self, obj):
        self._check_hashable(obj)
        if obj not in self._index:
            raise KeyError(f"{obj!r} is not in the priority queue")
        return self._heap[self._index[obj]][0]

    def __repr__(self):
        return f"PriorityQueue({self._heap!r})"

    # -----------------------------
    # helpers
    # -----------------------------
    def _check_hashable(self, obj):
        try:
            hash(obj)
        except TypeError:
            raise TypeError(
                f"Object {obj!r} is not hashable and cannot be used in PriorityQueue. "
                "Use immutable objects (str, int, tuple, etc.)."
            )

    # -----------------------------
    # heap index helpers
    # -----------------------------
    @staticmethod
    def _parent(i): return (i - 1) // 2
    @staticmethod
    def _left(i): return 2 * i + 1
    @staticmethod
    def _right(i): return 2 * i + 2

    def _swap(self, i, j):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
        _, obj_i = self._heap[i]
        _, obj_j = self._heap[j]
        self._index[obj_i] = i
        self._index[obj_j] = j

    def _bubble_up(self, i):
        while i > 0:
            p = self._parent(i)
            if self._heap[i][0] >= self._heap[p][0]:
                break
            self._swap(i, p)
            i = p

    def _bubble_down(self, i):
        n = len(self._heap)
        while True:
            left = self._left(i)
            right = self._right(i)
            smallest = i

            if left < n and self._heap[left][0] < self._heap[smallest][0]:
                smallest = left
            if right < n and self._heap[right][0] < self._heap[smallest][0]:
                smallest = right

            if smallest == i:
                break

            self._swap(i, smallest)
            i = smallest
