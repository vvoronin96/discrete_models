import matplotlib.pyplot as plt
import numpy as np

def statistisc(S):
    # --- STATISTICS ---

    #  --- store all in file  ---
    f = open('output.csv', 'w')
    f.write(
        "Id;Interarrival Time;Arrival Time;Service Time;Time Service Begins;Waiting time in Queue;Time Service Ends;Time Customer Spends in System;Idle time of Server;queueHistory\n")
    for s in S.stats:
        f.write("{0};{1};{2};{3};{4};{5};{6};{7};{8};{9}\n".format(s.id, s.interArrivalTime, s.arrivalTime, s.serviceTime,
                                                               s.serviceBegins, s.waitingTimeInQueue, s.serviceEnds,
                                                               s.timeInSystem, s.idleTimeOfServer, S.queueHistory))
    f.close()

    # 1) Average waiting time in queue
    avTimeInQueue = sum([x.waitingTimeInQueue for x in S.stats]) / len(S.stats)
    print('---------------')
    print("\nAverage waiting time\t{0:.2f}".format(avTimeInQueue))

    print(f'Mean size of queue\t{np.mean(S.queueHistory):.2f}')

    # 2) Probability that a customer has to wait
    probToWait = len([x for x in S.stats if x.waitingTimeInQueue > 0]) / len(S.stats)
    print("Probability that a customer has to wait\t{0:.2f}".format(probToWait))

    # 3) Probability of an Idle server
    probIdle = sum([x.idleTimeOfServer for x in S.stats]) / S.GlobalTime
    print("Probability of an Idle server\t{0:.2f}".format(probIdle))

    # 4) Average service time (theoretical 3.2)
    avServiceTime = sum([x.serviceTime for x in S.stats]) / len(S.stats)
    print("Average service time\t{0:.2f}".format(avServiceTime))

    # 5) Average time between arrivals (theoretical 4.5)
    avTimeBetwArr = sum([x.interArrivalTime for x in S.stats]) / (len(S.stats) - 1)
    print("Average time between arrivals\t{0:.2f}".format(avTimeBetwArr))

    # 6) Average waiting time for those who wait
    numOfCustWhoWait = len([x for x in S.stats if x.waitingTimeInQueue > 0])
    try:
        avTimeWhoWait = sum([x.waitingTimeInQueue for x in S.stats]) / numOfCustWhoWait
    except:
        avTimeWhoWait = 0
    print("Average waiting time for those who wait\t{0:.2f}".format(avTimeWhoWait))

    # 6)


    avTimeInTheSystem2 = avTimeInQueue + avServiceTime
    print("Average time a customer spends in the system (alternative)\t{0:.2f}".format(avTimeInTheSystem2))

    def DrawSampleHistogram(R, title, bins=None):
        fig = plt.figure()
        x = np.arange(len(R))
        plt.grid()
        if (bins is None):
            plt.hist(R, range=None)
        else:
            plt.hist(R, bins=bins, range=None)
        plt.title(title)
        plt.show()


    def cashier_plot(history):
        x = np.arange(len(history))
        plt.grid()
        plt.plot(x, history)
        plt.xlabel('Client')
        plt.ylabel('Number of cashier')
        plt.ylim(ymin = 2, ymax = 6)
        plt.show()

    cashier_plot(S.work_cashiers)
    DrawSampleHistogram([x.waitingTimeInQueue for x in S.stats], "Waiting time in queue")