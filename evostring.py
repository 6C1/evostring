import random, string
from math import ceil, floor, pow, sqrt
from time import sleep

def main():
    p = Population()
    i = 0
    while  p.current_population()[0] != p.phrase:
        sleep(0.2)
        i += 1
        p.mutate()
        p.sort()
        p.purge()
        p.shuffle()
        p.reproduce()
        p.sort()
        print p, '\n', p.min_dist(), i, '\n', p.phrase

class Population():
    history = []
    phrase = ''

    def __init__(self, phrase='teagan', init_pop=32):
        self.phrase = phrase
        # set up initial population
        result = []
        for i in xrange(init_pop):
            result.append(''.join(random.choice(string.ascii_letters) for j in xrange(len(self.phrase))))
        self.history.append(result)
    def __str__(self):
        result = '\n\n\n\n\n\n\n\n'
        result += result; result += result; result += result
        p = self.current_population()
        for i in xrange(0,7):
            s = p[-i]
            result += s + '\n\t\t' + str(pseudo_hamming(s, self.phrase)) + '\n'
        return result

    def mutate(self):
        for i in xrange(self.size()):
            s = self.history[-1][random.randrange(self.size())]
            n = random.randrange(len(s))
            new_char = chr( ord(s[n]) + random.randrange(-2,2) )
            s = s[0:n]+new_char+s[n+1:]
    def sort(self): self.history.append(sorted(self.current_population(), key=lambda x: pseudo_hamming(x, self.phrase)))
    def purge(self):
        self.history.append(self.current_population()[0:int(ceil(0.6763*self.size()))])
    def shuffle(self):
        random.shuffle(self.history[-1])
    def reproduce(self):
        n = int(floor(self.size() / 2.0))
        kids = []
        for i in xrange(n):
            a = self.current_population()[2*i]
            b = self.current_population()[2*i + 1]
            c = ''
            for j in xrange(len(self.phrase)):
                c += (chr(int(round( (ord(a[j])+ord(b[j]))/2.0) + random.randrange(-5,5))))
            kids.append(c)
        self.history.append(self.current_population()+kids)
        
    def range(self):
        return self.max_dist() - self.min_dist()
    def min_dist(self): return reduce(lambda x, y: min(x,y), map(lambda x: pseudo_hamming(x, self.phrase), self.current_population()))
    def max_dist(self): return reduce(lambda x, y: max(x,y), map(lambda x: pseudo_hamming(x, self.phrase), self.current_population()))
    def current_population(self): return self.history[-1]        
    def age(self): return len(self.history)
    def size(self): return len(self.current_population())

def pseudo_hamming(a, b):
    assert len(a) == len(b)
    return sum(char_dist(a[i],b[i]) for i in xrange(len(a)))
    
def char_dist(a, b):
    return abs(ord(a)-ord(b))

main()
