from random import uniform, randint
from simulator import simulator
import math         
class agent():
    def __init__(self, mdp, epsilon, beta, N, terminalS = None):
        self.q = []
        self.beta = beta
        self.epsilon = epsilon
        self.mdp = mdp
        self.S, self.A, _, _ = mdp
        self.numOfEpisodes = 100
        self.ts = terminalS
        self.alpha = 0.1
        for s in range(self.S):
            self.q.append([])
            for a in range(self.A):
                self.q[s].append(0)
        self.N = N
    def exploreOrExploitPolicy(self, cstate):
        p = uniform(0, 1)
        if p < self.epsilon:
            return randint(0, self.A - 1)
        else:
            return self.greedyPolicy(cstate)
        
    def greedyPolicy(self, cstate):
        maxV = max(self.q[cstate])
        for a, v in enumerate(self.q[cstate]):
            if maxV == v:
                return a
    
    def boltzmannExploration(self, cstate, num):
        T = 5 / (num + 1)
        pr = math.exp(self.q[cstate][0] * 0.01 / T) / (math.exp(self.q[cstate][0] * 0.01 / T) + math.exp(self.q[cstate][1] * 0.01 / T))
        if pr < uniform(0, 1):
            return 0
        else:
            return 1
    def initialState(self):
        if len(self.q) < 19:
            return 0
        pr = self.q[19][0]
        if uniform(0,1) < pr:
            return 0
        return 20
    def learningAndEvaluation(self):
        plotX = []
        plotY = []
        f = open("results/resultOf" + self.agentName + ".txt", "a")
        f.write("\n\n******** " + self.agentName + "(e = " + str(self.epsilon) + ", b = " + str(self.beta) + ")" + "********\n")
        for i in range(500):
 #           print(1)
            self.learningTrial()
            value = self.evaluation()
            f.write("---------- " + "After " + str((i + 1) * self.N) + " Trial Learning " + "----------------\n")
  #          print(self.q[0])
            f.write("Initial State Average Value:" + str(value) + "\n")
            plotY.append(value)
            plotX.append((i + 1) * self.N)
        f.write("************************************************************\n")
        f.close()
        return plotX, plotY

        
    def evaluation(self):
        rewards = 0
        for _ in range(self.numOfEpisodes):
            rewards += self.eachSimulation(300)
 #           print(rewards)

        averageR = rewards / self.numOfEpisodes
        return averageR

    def eachSimulation(self, maxSteps):
        _, A, _, _ = self.mdp
        steps = 0
        cs = self.initialState()
        reward = 0
        sim = simulator(self.mdp, currentS = cs, terminalS = self.ts)
        while steps < maxSteps:
 #           print(self.greedyPolicy(cs))
            res = sim.takeAction(self.greedyPolicy(cs))
            if res == "end":
                break
            elif res == "illegal":
                steps -= 1
            else:
                r, cs = res
                reward += (self.beta ** steps) * r
            steps += 1
           # print(steps)
        return reward
    
    def learningTrial(self):
        return 

class MCagent(agent):
    def __init__(self, mdp, epsilon, beta, N, terminalS = None):
        super().__init__(mdp, epsilon, beta, N, terminalS = None)
        self.totalq = []
        self.countq = []
        for s in range(self.S):
            self.totalq.append([])
            self.countq.append([])
            for a in range(self.A):
                self.totalq[s].append(0)
                self.countq[s].append(0)
        self.agentName = "Monte Carol Agent"
        
    def learningTrial(self):
        for _ in range(self.N):
            episode = []
            cstate = self.initialState()
            sim = simulator(self.mdp, currentS = cstate, terminalS = self.ts)
            T = 0
            visited = set()
            while True:
                a = self.exploreOrExploitPolicy(cstate)
                res = sim.takeAction(a)
                #print(res)
                if res == "end":
 #                   print(111)
                    break
                r, _ = res
                episode.append((cstate, a, r))
                _, cstate = res
                T += 1
                
  #          print(episode)
            for t in range(T):
                cstate, a, _ = episode[t]
                if (cstate, a) in visited:
                    continue
                visited.add((cstate, a))
                gt = 0
                for tt in range(t, T):
                    gt += episode[tt][2] * (self.beta ** (tt - t))
                self.totalq[cstate][a] += gt
                self.countq[cstate][a] += 1
                self.q[cstate][a] = self.totalq[cstate][a] / self.countq[cstate][a]

class SARSAagent(agent):
    def __init__(self, mdp, epsilon, beta, N, terminalS = None):
        super().__init__(mdp, epsilon, beta, N, terminalS = None)
        self.agentName = "SARSA Agent"
        
    def learningTrial(self):
        for _ in range(self.N):
            cs = self.initialState()
            a = self.exploreOrExploitPolicy(cs)
            sim = simulator(self.mdp, currentS = cs, terminalS = self.ts)
            while True:
 #               print(cs, sim.cs)
                res = sim.takeAction(a)
                if res == "end":
                    break
                r, ns = res
 #               print(cs, ns)
                na = self.exploreOrExploitPolicy(ns)
                self.q[cs][a] = self.q[cs][a] + self.alpha * (r + (self.beta * self.q[ns][na]) - self.q[cs][a])
                cs = ns
                a = na
                
class QLagent(agent):
    def __init__(self, mdp, epsilon, beta, N, terminalS = None):
        super().__init__(mdp, epsilon, beta, N, terminalS = None)
        self.agentName = "Q-learning Agent"
        
    def learningTrial(self):
        for _ in range(self.N):
            cs = self.initialState()
            sim = simulator(self.mdp, currentS = cs, terminalS = self.ts)
            while True:
 #               print(cs, sim.cs)
                a = self.exploreOrExploitPolicy(cs)
                res = sim.takeAction(a)
                if res == "end":
                    break
                r, ns = res
#                print(cs, ns)
                ga = self.greedyPolicy(ns)
                self.q[cs][a] = self.q[cs][a] + self.alpha * (r + (self.beta * self.q[ns][ga]) - self.q[cs][a])
                cs = ns

'''
class MCagent():
    def __init__(self, mdp, epsilon, N, terminalS = None):
        self.q = []
        self.totalq = []
        self.countq = []
        self.beta = 0.8
        self.epsilon = epsilon
        self.mdp = mdp
        self.S, self.A, _, _ = mdp
        self.numOfEpisodes = 100
        self.ts = terminalS
        for s in range(self.S):
            self.q.append([])
            self.totalq.append([])
            self.countq.append([])
            for a in range(self.A):
                self.q[s].append(0)
                self.totalq[s].append(0)
                self.countq[s].append(0)
        self.N = N
        

    def exploreOrExploitPolicy(self, cstate):
        p = uniform(0, 1)
        if p < self.epsilon:
            return randint(0, self.A - 1)
        else:
            return self.greedyPolicy(cstate)
        
    def greedyPolicy(self, cstate):
        maxV = max(self.q[cstate])
        for a, v in enumerate(self.q[cstate]):
            if maxV == v:
                return a
            
    def learningAndEvaluation(self):
        for i in range(300):
 #           print(1)
            self.learningTrial()
            value = self.evaluation()
            print(self.q[0])
            print(str(i + 1) + " learning " + str(value))

    def learningTrial(self):
        for _ in range(self.N):
            episode = []
            cstate = 0
            sim = simulator(self.mdp, terminalS = self.ts)
            T = 0
            visited = set()
            while True:
                a = self.exploreOrExploitPolicy(cstate)
                res = sim.takeAction(a)
                #print(res)
                if res == "end":
 #                   print(111)
                    break
                r, _ = res
                episode.append((cstate, a, r))
                _, cstate = res
                T += 1
                
  #          print(episode)
            for t in range(T):
                cstate, a, _ = episode[t]
                if (cstate, a) in visited:
                    continue
                visited.add((cstate, a))
                gt = 0
                for tt in range(t, T):
                    gt += episode[tt][2] * (self.beta ** (tt - t))
                    self.totalq[cstate][a] += gt
                    self.countq[cstate][a] += 1
                    self.q[cstate][a] = self.totalq[cstate][a] / self.countq[cstate][a]

    def evaluation(self):
        rewards = 0
        for _ in range(self.numOfEpisodes):
            rewards += self.eachSimulation(300)

        averageR = rewards / self.numOfEpisodes
        return averageR

    def eachSimulation(self, maxSteps):
        _, A, _, _ = self.mdp
        steps = 0
        cs = 0
        reward = 0
        sim = simulator(self.mdp, currentS = cs, terminalS = self.ts)
        while steps < maxSteps:
            res = sim.takeAction(self.greedyPolicy(cs))
            if res == "end":
                break
            elif res == "illegal":
                steps -= 1
            else:
                r, cs = res
                reward += (self.beta ** steps) * r
            steps += 1
           # print(steps)
        return reward
'''
