import random


# Queue of Events
class EventsQueue:
    def __init__(self):
        self.globalTime = 0
        self.MEvents = []

    def QueueSize(self):
        return len(self.MEvents)

    def AddEvent(self, MEvent):
        count = len(self.MEvents)
        if count == 0:
            self.MEvents.append(MEvent)
            return 0

        if (MEvent.eTime >= self.MEvents[count - 1].eTime):
            self.MEvents.append(MEvent)
            return 0

        for i in range(0, count - 1):
            if (MEvent.eTime >= self.MEvents[i].eTime):
                if (MEvent.eTime < self.MEvents[i + 1].eTime):
                    self.MEvents.insert(i + 1, MEvent)
                    return 0

    def ProcessNextEvent(self):
        if (len(self.MEvents) == 0):
            return 0
        self.MEvents[0].Execute()
        self.globalTime = self.MEvents[0].eTime
        del self.MEvents[0]


class Cashier:
    def __init__(self):
        self.isBusy = False
        self.isClosed = False


class CustomerQueue:
    def __init__(self, id):
        self.q = []
        self.id = id

    def length(self):
        return len(self.q)

    def pop(self):
        return self.q.pop(0)

    def append(self, cid):
        self.q.append(cid)


# Discrete Event System Specification
class DEVS:
    EQ = EventsQueue()
    GlobalTime = 0.0

    def __init__(self, one_queue=True, n_cashiers=4, closed_cashiers=[]):
        self.stats = []
        self.newId = 0
        self.lastServedTime = 0
        self.GlobalTime = 0.0
        self.EQ = EventsQueue()

        self.oneQueue = one_queue
        self.nCashiers = n_cashiers

        self.CustomerQueues = []
        if self.oneQueue:
            self.CustomerQueues = [CustomerQueue(0)]
        else:
            for i in range(self.nCashiers):
                self.CustomerQueues.append(CustomerQueue(i))

        self.Cashiers = []
        for i in range(self.nCashiers):
            self.Cashiers.append(Cashier())

        for i in closed_cashiers:
            self.Cashiers[i].isClosed = True

    @staticmethod
    def ProcessNextEvent():
        DEVS.EQ.ProcessNextEvent()
        DEVS.GlobalTime = DEVS.EQ.globalTime

    def ProcessNextEventNonStatic(self):
        self.EQ.ProcessNextEvent()
        self.GlobalTime = self.EQ.globalTime

    def isCashierFree(self, id):
        return not self.Cashiers[id].isBusy

    def isAnyCashierFree(self):
        return len([c for c in self.Cashiers if not c.isBusy and not c.isClosed]) > 0

    def randomCashier(self):
        return random.choice([i for i, c in enumerate(self.Cashiers) if not c.isClosed])

    def randomFreeCashier(self):
        return random.choice([i for i, c in enumerate(self.Cashiers) if not c.isClosed and not c.isBusy])

    def openCashier(self):
        closed_cashiers = [id for id, c in self.Cashiers if c.isClosed]
        if len(closed_cashiers) == 0: raise KeyError("All cashiers are open")
        self.Cashiers[random.choice(closed_cashiers)].isClosed = False

#    def closeCashier(self):
#        opened

    def shortestCashierQueue(self):
        if self.oneQueue: raise KeyError("There is just one line")
        return sorted(self.CustomerQueues, key=lambda x: x.length())[0].id

    def markCashierAsBusy(self, qid):
        if not self.Cashiers[qid].isBusy:
            self.Cashiers[qid].isBusy = True
        else:
            raise KeyError('Cashier is already busy')

    def markCashierAsFree(self, qid):
        if self.Cashiers[qid].isBusy:
            self.Cashiers[qid].isBusy = False
        else:
            raise KeyError('Cashier is already free')

    def lenOfQueue(self, qid=-1):
        if self.oneQueue:
            return self.CustomerQueues[0].length()
        else:
            return self.CustomerQueues[qid].length()

    def appendCustomer(self, customerId, qId=-1):
        if self.oneQueue:
            self.CustomerQueues[0].append(customerId)
        else:
            self.CustomerQueues[qId].append(customerId)

    def nextCustomer(self, qId=-1):
        if self.oneQueue:
            return self.CustomerQueues[0].pop()
        else:
            return self.CustomerQueues[qId].pop()
