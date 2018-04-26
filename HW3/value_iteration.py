
def VIfun(satr, outputV,outputP,beta = 0.9, epsilon = 0.01):
    S, A, T, R = satr
    optimalStates = 0
    
    while optimalStates < S:
        optimalStates = 0
        
        for s in range(S):
            if s in outputV:
                currentSPreV = outputV[s]
                maxV = float('-inf')
                maxA = -1
                for a in range(A):
 #                   print(s,a)
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
                    outputV = 0
                    outputP = None
                else:
                    outputP[s] = maxA
                    outputV[s] = maxV
            else:
                outputV[s] = 0
                outputP[s] = None
                currentSPreV = float('-inf')

            if (outputV[s] - currentSPreV) < epsilon:
 #               print(outputV[s],currentSPreV, epsilon)
                optimalStates += 1
#        print(optimalStates)
        
        

