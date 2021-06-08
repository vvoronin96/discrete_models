from EventsQueue import EventsQueue
from CustomerQueue import CustomerQueue

import random


class DEVS:
    EQ = EventsQueue()
    GlobalTime = 0.0

    def __init__(self, n_cashiers=4):
        # Parameters
        self.stats = []
        self.newId = 0
        self.lastServedTime = 0
        self.GlobalTime = 0.0
        self.nCashiers = n_cashiers
        self.queueHistory = []
        self.work_cashiers = []
        # Queues
        self.EQ = EventsQueue()
        self.CQ = CustomerQueue(0)

        # Cashiers
        # isIdle for cashier in nCashiers
        self.CASH = [True for _ in range(self.nCashiers)]

    def ProcessNextEvent(self):
        self.EQ.ProcessNextEvent()
        self.work_cashiers.append(self.nCashiers)
        self.GlobalTime = self.EQ.globalTime

    def isCashierFree(self, id): return self.CASH[id]
    def isAnyCashierFree(self): return len([c for c in self.CASH if c]) > 0
    def randomFreeCashier(self): return random.choice([i for i, c in enumerate(self.CASH) if c])

    def markCashierAsBusy(self, id):
        if not self.CASH[id]: raise KeyError('Cashier is already busy')
        self.CASH[id] = False

    def markCashierAsFree(self, id):
        if self.CASH[id]: raise KeyError('Cashier is already free')
        self.CASH[id] = True

    def appendCustomer(self, customerId): self.CQ.append(customerId)
    def nextCustomer(self): return self.CQ.pop()
    def lenOfQueue(self): return self.CQ.length()