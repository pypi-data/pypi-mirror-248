from . moby import get

class Names :
  def __init__(self) :
    self.names = get().names

  def __call__(self, count=None, transform=(lambda x: x)) :
    from random import sample

    return transform(
      sample(self.names, max(0, count))
      if count and count < len(self.names)
      else self.names
    )

def sortecle(seq) :
  seq = sorted(seq)
  c = True
  result = []
  used_up_indices = []

  while c :
    c = None
    for (i, s) in enumerate(seq) :
      if (i not in used_up_indices
          # word is not already appended to result

          and not (
            # duplicate first character
            c and s.startswith(c)
          )) :

        c = s[0]
        result.append(s)
        used_up_indices.append(i)

  return result

names = Names()

__all__ = ['names', 'sortecle']
