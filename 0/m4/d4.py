from EventsQueue import EventsQueue
from CustomerQueue import CustomerQueue


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
        # Event queue
        self.EQ = EventsQueue()

        # Cashiers
        # A tuple ((isIdle, isOpen)), CustomerQueue)
        self.CASHs = [((True, True), CustomerQueue(i)) for i in range(self.nCashiers)]
        # Close the last cashier for now
        self.CASHs[self.nCashiers - 1] = ((True, False), self.CASHs[self.nCashiers - 1][1])

    def ProcessNextEvent(self):
        self.EQ.ProcessNextEvent()
        self.work_cashiers.append(len([c for c in self.CASHs if c[0][1]]))
        self.GlobalTime = self.EQ.globalTime

    def isCashierFree(self, id): return self.CASHs[id][0][0]
    def isAnyCashierFree(self): return len([c for c in self.CASHs if c[0][0]]) > 0
    def shortestQueue(self):
        serv_events = [E.cashier_id for E in self.EQ.MEvents if type(E).__name__ == "ServiceEvent"]
        queue_lengths = [(c[1].i, c[1].length()) for c in self.CASHs]
        for i in serv_events:
            queue_lengths[i] = (queue_lengths[i][0], queue_lengths[i][1] + 1)

        return [c[0] for c in sorted(queue_lengths, key=lambda x: x[1])][0]

    def queueSizeForAll(self):
            return [(c[1].length()) for c in self.CASHs if c[1].length()>=0]

    def markCashierAsBusy(self, id):
        if not self.CASHs[id][0][0]: raise KeyError('Cashier is already busy')
        self.CASHs[id] = ((False, self.CASHs[id][0][1]), self.CASHs[id][1])

    def markCashierAsFree(self, id):
        if self.CASHs[id][0][0]: raise KeyError('Cashier is already free')
        self.CASHs[id] = ((True, self.CASHs[id][0][1]), self.CASHs[id][1])

    def openCashier(self):
        for i, c in enumerate(self.CASHs):
            if not c[0][1]:
                self.CASHs[i] = ((self.CASHs[i][0][0], True), self.CASHs[i][1])
                return

        raise KeyError('Nothing to open')

    def closeCashier(self):
        for i, c in enumerate(self.CASHs):
            if c[0][1]:
                self.CASHs[i] = ((self.CASHs[i][0][0], False), self.CASHs[i][1])
                return

        raise KeyError('Nothing to close')

    def manageCashiers(self):
        len_busy_cashiers = len([c for c in self.CASHs if not c[0][0]])
        len_open_cashiers = len([c for c in self.CASHs if c[0][1]])
        len_free_cashiers = len([c for c in self.CASHs if c[0][0] and c[0][1]])

        if len_open_cashiers > 4 and len_free_cashiers > 0:
            self.closeCashier()

        if len_busy_cashiers == 4 and len_open_cashiers == 4:
            self.openCashier()

    def appendCustomer(self, customerId, qid): self.CASHs[qid][1].append(customerId)
    def nextCustomer(self, qid): return self.CASHs[qid][1].pop()
    def lenOfQueue(self, qid): return self.CASHs[qid][1].length()
