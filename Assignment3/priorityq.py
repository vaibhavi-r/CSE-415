'''priorityq.py
A module that provides a custom priority queue implementation
for use in A* and similar algorithms.

Version of Oct. 17, 2017, which contains
an adjustment to handle duplicate priority values
together with elements that don't implement
the __lt__ method.

Ties are broken by adding a small random adjustment value
to the new priority value.  These adjustments are less than
0.00001.

 By S. Tanimoto,
'''

import heapq, random

class PriorityQ:
  def __init__(self):
    self.elts = []
    self.keys = {}

  def isEmpty(self):
    return len(self.elts)==0

  def insert(self, element, priority):
    try:
      heapq.heappush(self.elts, (priority, element))
    except TypeError as e:
      # resolve priority ties by adding a small random increment to the new one.
      adjustment = random.uniform(0.000001, 0.000009)
      heapq.heappush(self.elts, (priority+adjustment, element))
    self.keys[element]=True

  def deletemin(self):
    try:
      item = heapq.heappop(self.elts)
    except TypeError as e:
      # A tie should never show up here, having been broken during the insert.
      # but if does, this fix should work.  It did during some testing
      # before the insertion tie-breaking was made.
      item = self.elts[0]
      del self.elts[0]

    (priority, element) = item

    self.keys.pop(element, None)
    return element

  def __contains__(self, element):
    return element in self.keys

  def __str__(self):
    return 'PriorityQ'+str(self.elts)

def test():
  q = PriorityQ()
  q.insert('A', 5)
  q.insert('B', 4)
  q.insert('C', 6)

  print("B in Q is "+str('B' in q))
  print("C in Q is "+str('C' in q))
  print("D in Q is "+str('D' in q))

  print(q)

  print(q.deletemin())
  print("B in Q is "+str('B' in q))
  print(q.deletemin())
  print(q.deletemin())

if __name__ == "__main__": test()
