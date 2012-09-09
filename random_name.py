from random import choice, randint

ADJECTIVES =  [
  'hip',
  'crazy',
  'cool',
  'fun',
  'happy',
  'uber',
  'captain',
  'fierce',
  'amazing',
  'fantastic',
  'big',
  'mister',
  'phat',
  'friendly',
  'amiable',
  'upbeat',
  'hyper',
  'chill',
  'relaxed',
  'tremendous',
  'outstanding',
  'little'
]

NOUNS = [
  'cat',
  'dawg',
  'pants',
  'head',
  'fish',
  'player',
  'dude',
  'animal',
  'gamer',
]

def generate():
  adjectives = _get_adjectives()
  noun = choice(NOUNS)
  name = '%s %s' % (adjectives, noun)
  name = name.title().replace(' ', '')
  return name

def _get_adjectives():
  # 1 90%
  # 2 9%
  # 3 1%
  rand100 = randint(0, 100)
  if rand100 <= 90:
    num_adjectives = 1
  elif rand100 <= 99:
    num_adjectives = 2
  else:
    num_adjectives = 3
  adjectives = ' '.join([choice(ADJECTIVES) for _ in range(num_adjectives)])
  return adjectives

if __name__ == '__main__':
  for i in xrange(200):
    print generate()
