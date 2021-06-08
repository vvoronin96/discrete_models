from EventsQueue import EventsQueue
from CustomerQueue import CustomerQueue

import random


class DEVS:
    EQ = EventsQueue()
    GlobalTime = 0.0

    def __init__(self, n_cashiers=5):
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
        # (isIdle, isOpen) for cashier in nCashiers
        self.CASH = [(True, True) for _ in range(self.nCashiers)]
        # close the last cashier for now
        self.CASH[self.nCashiers - 1] = (True, False)

    def ProcessNextEvent(self):
        self.EQ.ProcessNextEvent()
        self.work_cashiers.append(len([c for c in self.CASH if c[1]]))
        self.GlobalTime = self.EQ.globalTime

    def isCashierFree(self, id): return self.CASH[id]
    def isAnyCashierFree(self): return len([c for c in self.CASH if c[0]]) > 0
    def randomFreeCashier(self): return random.choice([i for i, c in enumerate(self.CASH) if c[0]])

    def markCashierAsBusy(self, id):
        if not self.CASH[id][0]: raise KeyError('Cashier is already busy')
        self.CASH[id] = (False, self.CASH[id][1])

    def markCashierAsFree(self, id):
        if self.CASH[id][0]: raise KeyError('Cashier is already free')
        self.CASH[id] = (True, self.CASH[id][1])

    def openCashier(self):
        for i, c in enumerate(self.CASH):
            if not c[1]:
                self.CASH[i] = (c[0], True)
                return

        raise KeyError('Nothing to open')

    def closeCashier(self):
        for i, c in enumerate(self.CASH):
            if c[1]:
                self.CASH[i] = (c[0], False)
                return

        raise KeyError('Nothing to close')

    def manageCashiers(self):
        len_busy_cashiers = len([c for c in self.CASH if not c[0]])
        len_open_cashiers = len([c for c in self.CASH if c[1]])
        len_free_cashiers = len([c for c in self.CASH if c[0] and c[1]])

        if len_open_cashiers > 4 and len_free_cashiers > 0:
            self.closeCashier()

        if len_busy_cashiers == 4 and len_open_cashiers == 4:
            self.openCashier()

    def appendCustomer(self, customerId): self.CQ.append(customerId)
    def nextCustomer(self): return self.CQ.pop()
    def lenOfQueue(self): return self.CQ.length()