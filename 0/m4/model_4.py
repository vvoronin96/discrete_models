"""

Динмическая модель с выбором самой короткой очереди

Правило 1: если все кассы заняты, открывается еще одна
Правило 2: если свободно более чем, две кассы, резервная касса закрывается
Правило 3: резервная касса только одна

Покупатель идет на кассу с самой короткой очередью

"""



from m4.d4 import DEVS
from customerStat import customerStat
from Statistics import statistisc

import numpy as np
from scipy import stats

maxAngents = 10000

arrival_min = 0.2
arrival_max = 1.5
arrival_rate = stats.uniform(loc = arrival_min, scale = arrival_max)
service_xk = np.arange(6) + 1.1
service_pk = (0.1, 0.2, 0.25, 0.3, 0.1, 0.05)
custm = stats.rv_discrete(name='custm', values=(service_xk, service_pk))


# ---- Arrival Event ----
class ArrivalEvent:
    def __init__(self):
        self.eTime = 0.0

    def Execute(self):
        customer = customerStat()
        customer.id = S.newId
        customer.arrivalTime = self.eTime
        if len(S.stats) > 0:
            customer.interArrivalTime = customer.arrivalTime - S.stats[-1].arrivalTime

        print("Time %d" % self.eTime, " Arrival Event of agent {0}".format(customer.id))
        if S.newId < maxAngents - 1:
            NextArrival = ArrivalEvent()
            NextArrival.eTime = self.eTime + arrival_rate.rvs()
            S.EQ.AddEvent(NextArrival)

        # open or close cashiers when needed
        S.manageCashiers()

        shortest_q_id = S.shortestQueue()
        if S.isCashierFree(shortest_q_id):
            # getting a random free cashier queue
            S.markCashierAsBusy(shortest_q_id)
            print(f'Cashier #{shortest_q_id} is busy')

            Service = ServiceEvent(shortest_q_id)
            serviceTime = custm.rvs()

            customer.serviceTime = serviceTime
            customer.serviceBegins = self.eTime  # current time

            Service.eTime = self.eTime + serviceTime
            Service.id = customer.id

            S.EQ.AddEvent(Service)
        else:
            # increase waiting line for that casheer
            S.appendCustomer(customer.id, shortest_q_id)
            print(f'For customer queue #{shortest_q_id} line length is {S.lenOfQueue(shortest_q_id)}')

        S.queueHistory.append(np.mean(S.queueSizeForAll())+0.5)
        S.newId = S.newId + 1
        S.stats.append(customer)


# ---- Service (END) Event ----
class ServiceEvent:
    def __init__(self, c_id):
        self.eTime = 0.0
        self.id = 0
        self.cashier_id = c_id

    def Execute(self):
        ind = [i for i, val in enumerate(S.stats) if val.id == self.id][0]
        S.stats[ind].serviceEnds = self.eTime
        S.stats[ind].timeInSystem = S.stats[ind].serviceEnds - S.stats[ind].arrivalTime
        S.stats[ind].waitingTimeInQueue = S.stats[ind].serviceBegins - S.stats[ind].arrivalTime  # 0 without queue
        if S.stats[ind].serviceBegins - S.lastServedTime > 0:
            S.stats[ind].idleTimeOfServer = S.stats[ind].serviceBegins - S.lastServedTime
        else:
            S.stats[ind].idleTimeOfServer = 0

        print(f"Time {self.eTime} Service of cashier #{self.cashier_id} finished")

        if S.lenOfQueue(self.cashier_id) > 0:
            customer_id = S.nextCustomer(self.cashier_id)
            qind = [i for i, val in enumerate(S.stats) if val.id == customer_id][0]

            Service = ServiceEvent(self.cashier_id)
            serviceTime = custm.rvs()

            Service.eTime = self.eTime + serviceTime
            Service.id = customer_id

            S.stats[qind].serviceBegins = self.eTime
            S.stats[qind].serviceTime = serviceTime

            S.EQ.AddEvent(Service)
            print("take new customer from the queue")
        else:
            S.markCashierAsFree(self.cashier_id)
            print(f"Cashier #{self.cashier_id} is idle")

        S.lastServedTime = self.eTime


# init system
S = DEVS()

# run simulation
AE = ArrivalEvent()
S.EQ.AddEvent(AE)

# --- SIMULATION ---
while S.EQ.QueueSize() > 0:
    S.ProcessNextEvent()

statistisc(S)