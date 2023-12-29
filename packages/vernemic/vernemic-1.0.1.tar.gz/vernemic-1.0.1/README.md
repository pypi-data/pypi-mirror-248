# Mnemonic Version Names #

I have always wondered if it was easier to remember
(and distinguish between) numbers like 48 and 32 in
contrast with names like _holmes_ and _geneva_. This
program is a little experiment to generate an easy
plugin to situations where a random hex or a numeric
iterator is a natural decision for lack of a better
choice. For example,

```python
from vernemic import names
for name in names(count) :
  pass
  
# or
for i, name in enumerate(names(count, sorted)) :
  pass

# instead of 
for i in range(count) :
  pass
```

## Sorted with cycle ##
The version names start with `a`, `b` ... and start
back again from the top. Its not as if each character
is repeated; but whatever is available is cycled. For
example,

```
['amandi', 'burdett', 'clothilde', 'encratis',
 'georglana', 'inglis', 'jaquiss', 'kondon', 'lunn',
 'maure', 'ponzo', 'sally', 'erland', 'gladys',
 'justin', 'lyns', 'sussi', 'gunzburg', 'gyasi']
```

# Design Choices #

## Corpus ##
The names corpus is taken from [the Moby II
project](https://en.wikipedia.org/wiki/Moby_Project#Words)

### Folder Structure ###

By default `ROOT=~/.moby`

```
ROOT
+-  moby.tar.Z
\-  Moby
    +-  [...]
    \-  mwords
        +-  [...]
        +-  21986na.mes
```
