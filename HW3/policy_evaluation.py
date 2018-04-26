
def PEfun_VI(satr, vpi, pi, beta = 0.9, epsilon = 0.01):
    S, A, T, R = satr
    optimalStates = 0
    while optimalStates < S:
        optimalStates = 0
        for s in range(S):
            if s in vpi:
                currentSPreV = vpi[s]
                reward = R[s][pi[s]]
                expectedFuture = 0
                for sp, pr in enumerate(T[pi[s]][s]):
                    if pr != 0 and sp in vpi:
                        expectedFuture += pr * vpi[sp]
                vpi[s] = reward + (beta * expectedFuture)
                
                if (vpi[s] - currentSPreV) < epsilon:
                    optimalStates += 1
            else:
                vpi[s] = 0

            
