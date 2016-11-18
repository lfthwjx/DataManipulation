import re

str = 'a simple example.'
match = re.search(r'\.',str)
match = re.search(r'simple', str)
match = re.search(r'a',str)
if match:
    print 'found'


s = '@taggest!!!!!!'
s = 'The eerie wind said Oooo and Rrr'
match = re.findall(r'[aeiou]{2,}',s)
#match
def leading_and_trailing(s):
    s = s.lower()
    return bool(re.match('^[a-z]\w+(er|est!*)$',s))

def parse_counted_words(s):
  # Your code here: make sure to modify the return statement to pass back
  # the correct value.
  return None