from random import uniform
class simulator():
    def __init__(self, mdp, terminalS = None, currentS = 0):
        self.mdp = mdp
        self.ts = terminalS
        self.cs = currentS
        self.isTerminal = False
        if self.ts == self.cs:
            self.isTerminal = True
    def run(self, agent):
        self.agent = agent
    def takeAction(self, a):
        if self.isTerminal:
            return "end"
        S, A, T, R = self.mdp
 #       print(self.cs, a)
        reward = R[self.cs][a]
        probability = T[a][self.cs]
        if sum(probability) == 0:
 #           print(self.cs, a)
            return "illegal"
        
        nextStates = []
        nextStatesRate = []
        
        '''all posible next state'''
        for ns in range(S):
            if T[a][self.cs][ns] > 0:
                nextStates.append(ns)
                nextStatesRate.append(T[a][self.cs][ns])
        ''' choosing next state base on probability'''
        pr = uniform(0, 1)
        sump = 0
        for i, p in enumerate(nextStatesRate):
            sump += p
            if pr < sump:
                ns = nextStates[i]
                break
        '''cheking terminal state'''
        self.cs = ns
        if self.cs == self.ts:
            self.isTerminal = True
        sumOfPr = 0
        if not self.isTerminal:
            for a in range(A):
                for s in range(S):
                    sumOfPr += T[a][self.cs][s]
            
            if sumOfPr == 0:
 #               print(sumOfPr)
                self.isTerminal = True

        return (reward, self.cs)
        
