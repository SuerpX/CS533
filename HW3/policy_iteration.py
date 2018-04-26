from policy_evaluation import PEfun_VI
def PIfun(satr, outputV, outputP, beta = 0.9, epsilon = 0.01):
    S, A, T, R = satr
    for s in range(S):
        outputP[s] = 0
    optimalStates = 0
    while optimalStates < S:
        PEfun_VI(satr, outputV, outputP, beta, epsilon)
        for s in range(S):
 #           print(outputP)
            currentSPreP = outputP[s]
            maxV = float('-inf')
            maxA = -1
            for a in range(A):
                reward = R[s][a]
                expectedFuture = 0
                for sp, pr in enumerate(T[a][s]):
                    if pr != 0 and sp in outputV:
                        expectedFuture += pr * outputV[sp]
                value = reward + (beta * expectedFuture)
                if value > maxV:
                    maxV = value
                    maxA = a
            if maxA == -1:
                outputP[s] = None
            else:
                outputP[s] = maxA
        if outputP[s] == currentSPreP:
            optimalStates += 1
