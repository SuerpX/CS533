from random import randint, uniform
DRIVE = 0
PARK = 1
def policySelector(policyName):
 #   print(policyName)
    if policyName == "random":
#        print(1111)
        return randomPolicy
    elif policyName == "parkingRandomPolicy":
        return parkingRandomPolicy
    elif policyName == "parkingAvoidingOccupuiedPolicy":
        return parkingAvoidingOccupuiedPolicy
    elif policyName == "parkingSimpleImpovementPolicy":
        return parkingSimpleImpovementPolicy


def randomPolicy(mdp, state, p = None):
    S,A,T,R = mdp
#    print(A)
    return randint(0, A - 1)

def parkingRandomPolicy(mdp, state, p = 0.1):
    S, A, T, R = mdp
    if uniform(0,1) < p:
        return PARK
    return DRIVE

def parkingAvoidingOccupuiedPolicy(mdp, state, p = 0.1):
    S, A, T, R = mdp
    if state >= 20:
        return DRIVE
    elif uniform(0,1) < p:
        return PARK
    return DRIVE

def parkingSimpleImpovementPolicy(mdp, state, p = 0.1):
    S, A, T, R = mdp
    if state >= 20 or state in{9,10}:
        return DRIVE
    if state in {6, 7, 8, 11, 12, 13}:
        return PARK
    if uniform(0,1) < p:
        return PARK
    return DRIVE





    
