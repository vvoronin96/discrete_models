class CustomerQueue:
    def __init__(self, i):
        self.q = []
        self.i = i

    def length(self):
        return len(self.q)

    def pop(self):
        return self.q.pop(0)

    def append(self, cid):
        self.q.append(cid)
