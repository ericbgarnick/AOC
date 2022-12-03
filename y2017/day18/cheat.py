import collections

instructions = open("day18/data18.txt").read().strip().splitlines()


def program(pid, inqueue, outqueue):
    r = collections.defaultdict(int)
    r['p'] = pid
    val = lambda v: r[v] if v.isalpha() else int(v)

    i = 0
    while 0 <= i < len(instructions):
        f, X, Y, *_ = (instructions[i] + " ?").split()
        if f == 'set':      r[X] = val(Y)
        elif f == 'add':    r[X] += val(Y)
        elif f == 'mul':    r[X] *= val(Y)
        elif f == 'mod':    r[X] %= val(Y)
        elif f == 'jgz' and val(X) > 0:     i += val(Y) - 1
        elif f == 'snd':
            outqueue.append(val(X))
            yield 'send'
        elif f == 'rcv':
            while not inqueue:
                yield 'wait'
            else:
                r[X] = inqueue.popleft()
                yield 'recd'
        i += 1


q1 = collections.deque()
for s in program(0, q1, q1):
    if s == 'recd': break
print(q1[-1])

q0, q1 = collections.deque(), collections.deque()
P0, P1 = program(0, q1, q0), program(1, q0, q1)
i, count = 0, 0
while True:
    a, b = next(P1), next(P0)
    count += a == 'send'
    if {a, b} == {'wait'}:
        break
print(count)
