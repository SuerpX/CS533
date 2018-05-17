from loadMDP import loadMDP
from simulator import simulator
from random import randint
from policies import policySelector
import parking_MDP
from agnets import MCagent, SARSAagent, QLagent
from plot import generatePlot


def run_policy_simulation(filename, policy, beta, numOfEpisodes, maxSteps, pOfParkingRandom, terminalState = None):

    mdp = loadMDP(filename)
    res = simulation(mdp, policy, beta = beta, numOfEpisodes = numOfEpisodes, maxSteps = maxSteps, pOfParkingRandom = pOfParkingRandom, terminalState = terminalState)
    resf.write("**********" + filename[: -4] + "[policy: " + policy + "]" + (" (p = " + str(pOfParkingRandom) + ")" if "parking" in filename else "") + "*********\n")
    resf.write("Average reward: " + str(res) + "\n")
    resf.write("*********************************************\n\n")


def simulation(mdp, policy, beta = 0.9, numOfEpisodes = 100, maxSteps = 100, pOfParkingRandom = 0.9, terminalState = None):
    rewards = 0
    p = policySelector(policy)
 #   print(p)
    for _ in range(numOfEpisodes):
        rewards += eachSimulation(mdp, p, beta, maxSteps, pOfParkingRandom, terminalState)

    averageR = rewards / numOfEpisodes
    return averageR

def eachSimulation(mdp, p, beta, maxSteps, pOfParkingRandom, terminalState):
    _, A, _, _ = mdp
    steps = 0
    cs = 0
    reward = 0
    sim = simulator(mdp, currentS = cs,terminalS = terminalState)
    while steps < maxSteps:
        res = sim.takeAction(p(mdp,cs, p = pOfParkingRandom))
        if res == "end":
            break
        elif res == "illegal":
            steps -= 1
        else:
            r, cs = res
            reward += (beta ** steps) * r
        steps += 1
    return reward

def funRL(agent, filename, epsilon, beta, N, terminalS = None):
    mdp = loadMDP(filename)
    if agent == "MCagent":
        return MCagent(mdp, epsilon, beta, N, terminalS).learningAndEvaluation()
    elif agent == "SARSAagent":
        return SARSAagent(mdp, epsilon, beta, N, terminalS).learningAndEvaluation()
    elif agent == "QLagent":
        return QLagent(mdp, epsilon, beta, N, terminalS).learningAndEvaluation()

def main():
    
    
    run_policy_simulation("mdp_test.txt", "random", 0.8, 300, 300, 0.9, terminalState = 4)

    run_policy_simulation("parking_mdp1.txt", "parkingRandomPolicy", 1, 300, 300, 0.1)
    #run_policy_simulation("parking_mdp1.txt", "parkingRandomPolicy", 1, 200, 300, 0.9)
    run_policy_simulation("parking_mdp2.txt", "parkingRandomPolicy", 1, 300, 300, 0.1)
    #run_policy_simulation("parking_mdp2.txt", "parkingRandomPolicy", 1, 200, 300, 0.9)

    run_policy_simulation("parking_mdp1.txt", "parkingAvoidingOccupuiedPolicy", 1, 300, 300, 0.1)
    #run_policy_simulation("parking_mdp1.txt", "parkingAvoidingOccupuiedPolicy", 1, 200, 300, 0.9)
    run_policy_simulation("parking_mdp2.txt", "parkingAvoidingOccupuiedPolicy", 1, 300, 300, 0.1)
    #run_policy_simulation("parking_mdp2.txt", "parkingAvoidingOccupuiedPolicy", 1, 200, 300, 0.9)

    run_policy_simulation("parking_mdp1.txt", "parkingSimpleImpovementPolicy", 1, 300, 300, 0.1)
    #run_policy_simulation("parking_mdp1.txt", "parkingSimpleImpovementPolicy", 1, 200, 300, 0.9)
    run_policy_simulation("parking_mdp2.txt", "parkingSimpleImpovementPolicy", 1, 300, 300, 0.1)
    #run_policy_simulation("parking_mdp2.txt", "parkingSimpleImpovementPolicy", 1, 200, 300, 0.9)
    resf.close()
    print("25%")
    
    N = 1
    N2 = 50
 #   N3 = 50000
    
    x11, y11 = funRL("MCagent", "mdp_test.txt", 0.05, 0.8, N, terminalS = 4)
    x12, y12 = funRL("SARSAagent", "mdp_test.txt", 0.05, 0.8, N, terminalS = 4)
    x13, y13 = funRL("QLagent", "mdp_test.txt", 0.05, 0.8, N, terminalS = 4)
    generatePlot(x11, y11, x12, y12, x13, y13, "mdp_test (e = 0.05)")
    print("generted plot")
    print("40%")
    x21, y21 = funRL("MCagent", "mdp_test.txt", 0.3, 0.8, N, terminalS = 4)
    x22, y22 = funRL("SARSAagent", "mdp_test.txt", 0.3, 0.8, N, terminalS = 4)
    x23, y23 = funRL("QLagent", "mdp_test.txt", 0.3, 0.8, N, terminalS = 4)
    generatePlot(x21, y21, x22, y22, x23, y23, "mdp_test (e = 0.3)")
    print("generted plot")
    print("55%")
    x31, y31 = funRL("MCagent", "parking_mdp1.txt", 0.05, 0.999, N2)
    x32, y32 = funRL("SARSAagent", "parking_mdp1.txt", 0.05, 0.999, N2)
    x33, y33 = funRL("QLagent", "parking_mdp1.txt", 0.05, 0.999, N2)
    generatePlot(x31, y31, x32, y32, x33, y33, "parking_mdp1 (e = 0.05)")
    print("generted plot")
    print("70%")
    x41, y41 = funRL("MCagent", "parking_mdp1.txt", 0.3, 0.999, N2)
    x42, y42 = funRL("SARSAagent", "parking_mdp1.txt", 0.3, 0.999, N2)
    x43, y43 = funRL("QLagent", "parking_mdp1.txt", 0.3, 0.999, N2)
    generatePlot(x41, y41, x42, y42, x43, y43, "parking_mdp1 (e = 0.3)")
    print("generted plot")
    print("80%")
    x51, y51 = funRL("MCagent", "parking_mdp2.txt", 0.05, 0.999, N2)
    x52, y52 = funRL("SARSAagent", "parking_mdp2.txt", 0.05, 0.999, N2)
    x53, y53 = funRL("QLagent", "parking_mdp2.txt", 0.05, 0.999, N2)
    generatePlot(x51, y51, x52, y52, x53, y53, "parking_mdp2 (e = 0.05)")
    print("generted plot")
    print("90%")
    x61, y61 = funRL("MCagent", "parking_mdp2.txt", 0.3, 0.999, N2)
    x62, y62 = funRL("SARSAagent", "parking_mdp2.txt", 0.3, 0.999, N2)
    x63, y63 = funRL("QLagent", "parking_mdp2.txt", 0.3, 0.999, N2)
    generatePlot(x61, y61, x62, y62, x63, y63, "parking_mdp2 (e = 0.3)")
    print("generted plot")
    print("100%")
    
    

resf = open("results/resultOfPolicySimulation.txt", 'w')
main()


