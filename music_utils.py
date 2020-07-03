def flatten(l):
  def _flatten(_l):
    try:
      for item in l:
        yield from flatten(item)
    except TypeError:
      yield l
  return list(_flatten(l))

def enlengthen(l, factor):
  return list(map(lambda x: [x]*factor, l))

