import sys
import inspect
import heapq, random

class PriorityQueue:
    """
    Implements a priority queue data structure. Each inserted item
    has a priority associated with it and the client is usually interested
    in quick retrieval of the lowest-priority item in the queue. This
    data structure allows O(1) access to the lowest-priority item.

    Note that this PriorityQueue does not allow you to change the priority
    of an item.  However, you may insert the same item multiple times with
    different priorities.
    """

    def __init__(self):
        self.heap = []
        self.init = False

    def push(self, item, priority):
        if not self.init:
            self.init = True
            try:
                item < item
            except:
                item.__class__.__lt__ = lambda x, y: (True)
        pair = (priority, item)
        heapq.heappush(self.heap, pair)

    def pop(self):
        (priority, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0


class Counter(dict):
    """
    A counter keeps track of counts for a set of keys.
    The counter class is an extension of the standard python
    dictionary type.  It is specialized to have number values
    (integers or floats), and includes a handful of additional
    functions to ease the task of counting data.  In particular,
    all keys are defaulted to have value 0.
    The counter also includes additional functionality useful in implementing
    the classifiers for this assignment.  Two counters can be added,
    subtracted or multiplied together.  See below for details.  They can
    also be normalized and their total count and arg max can be extracted.
    """
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)

    def increment_all(self, keys, count):
        """ Increments all elements of keys by the same count. """
        for key in keys:
            self[key] += count

    def arg_max(self):
        """ Returns the key with the highest value. """
        if len(self.keys()) == 0: return None
        all = list(self.items())
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]

    def sorted_keys(self):
        """
        Returns a list of keys sorted by their values.
        Keys with the highest values will appear first.
        """
        sortedItems = list(self.items())
        sortedItems.sort(key=lambda item: -item[1])
        return [x[0] for x in sortedItems]

    def total_count(self):
        """ Returns the sum of counts for all keys. """
        return sum(self.values())

    def normalize(self):
        """
        Edits the counter such that the total count of all
        keys sums to 1.  The ratio of counts for all keys
        will remain the same. Note that normalizing an empty
        Counter will result in an error.
        """
        total = float(self.total_count())
        if total == 0: return
        for key in self.keys():
            self[key] = self[key] / total

    def divideAll(self, divisor):
        """
        Divides all counts by divisor
        """
        divisor = float(divisor)
        for key in self:
            self[key] /= divisor

    def copy(self):
        """
        Returns a copy of the counter
        """
        return Counter(dict.copy(self))

    def __mul__(self, y):
        """
        Multiplying two counters gives the dot product of their vectors where
        each unique label is a vector element.
        """
        sum = 0
        x = self
        if len(x) > len(y):
            x, y = y, x
        for key in x:
            if key not in y:
                continue
            sum += x[key] * y[key]
        return sum

    def __radd__(self, y):
        """
        Adding another counter to a counter increments the current counter
        by the values stored in the second counter.
        """
        for key, value in y.items():
            self[key] += value

    def __add__(self, y):
        """
        Adding two counters gives a counter with the union of all keys and
        counts of the second added to counts of the first.
        """
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] + y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = y[key]
        return addend

    def __sub__(self, y):
        """
        Subtracting a counter from another gives a counter with the union of all keys and
        counts of the second subtracted from counts of the first.
        """
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] - y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = -1 * y[key]
        return addend


def flipCoin(p):
    r = random.random()
    return r < p


# ## code to handle timeouts
# import signal
#
#
# class TimeoutFunctionException(Exception):
#     """Exception to raise on a timeout"""
#     pass
#
#
# class TimeoutFunction:
#
#     def __init__(self, function, timeout):
#         "timeout must be at least 1 second. WHY??"
#         self.timeout = timeout
#         self.function = function
#
#     def handle_timeout(self, signum, frame):
#         raise TimeoutFunctionException()
#
#     def __call__(self, *args):
#         if not 'SIGALRM' in dir(signal):
#             return self.function(*args)
#         old = signal.signal(signal.SIGALRM, self.handle_timeout)
#         signal.alarm(self.timeout)
#         try:
#             result = self.function(*args)
#         finally:
#             signal.signal(signal.SIGALRM, old)
#         signal.alarm(0)
#         return result
