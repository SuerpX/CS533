def parkingMDP(n, paras1, paras2):
    
    def _parkingMDP(n, paras):
        S = 8 * n
        A = 2

        T = []
        #init, T(currentS, a, targetS) = 0, R(s, a) = 0
        for a in range(A):
            T.append([])
            for curS in range(S):
                T[a].append([])
                for tarS in range(S):
                    T[a][curS].append(0)
        R = []
        for s in range(S):
            R.append([])
            for a in range(A):
                R[s].append(0)
        #driving
        #no occupation state, from 0 to 2n - 1
        #occupation state, from 2n to 2n - 1 + 2n
        for i in range(0, n - 2):
            T[0][i][i + 1] = 1 - (paras[0] * (i + 1))
            T[0][i + 2 * n][i + 1] = 1 - (paras[0] * (i + 1))
            T[0][i][i + 1 + 2 * n] = paras[0] * (i + 1)
            T[0][i + 2 * n][i + 1 + 2 * n] = paras[0] * (i + 1)
            
        T[0][n - 2][n - 1] = 1 - (paras[1])
        T[0][n - 1][n] = 1 - (paras[1])
        T[0][n - 2 + 2 * n][n - 1 + 2 * n] = paras[1]
        T[0][n - 1 + 2 * n][n + 2 * n] = paras[1]
        
        T[0][n - 2][n - 1 + 2 * n] = paras[1]
        T[0][n - 1][n + 2 * n] = paras[1]
        T[0][n - 2 + 2 * n][n - 1] = 1 - paras[1]
        T[0][n - 1 + 2 * n][n ] = 1 - paras[1]


        for i in range(n, 2 * n - 1):
            T[0][i][i + 1] = paras[0] * (i - n + 1)
            T[0][i + 2 * n][i + 1 + 2 * n] = 1 - (paras[0] * (i - n + 1))
            T[0][i][i + 1 + 2 * n] = 1 - (paras[0] * (i - n + 1))
            T[0][i + 2 * n][i + 1] = paras[0] * (i - n + 1)
        #
        T[0][2 * n - 1][0] = paras[0] * (n - 1)
        T[0][2 * n - 1 + 2 * n][0 + 2 * n] = 1 - (paras[0] * (n - 1))
        T[0][2 * n - 1][0 + 2 * n] = 1 - (paras[0] * (n - 1))
        T[0][2 * n - 1 + 2 * n][0] = paras[0] * (n - 1)
        #parking
        for i in range(0, 4 * n):
            T[1][i][i + 4 * n] = 1 

        #reward
        for s in range(0, 4 * n):
            R[s][0] = paras[3]
            
        for s in range(0, n - 1):
            R[s][1] = paras[2][1] * (s + 1) + (paras[2][0] - (n - 1) * paras[2][1])
            R[s + 2 * n][1] = paras[2][1] * (s + 1) + (paras[2][0] - (n - 1) * paras[2][1]) + paras[4]
        R[n - 1][1] = paras[5]
        R[n][1] = paras[5]
        R[n - 1 + 2 * n][1] = paras[5] + paras[4]
        R[n + 2 * n][1] = paras[5] + paras[4]
        for s in range(n + 1, 2 * n):
            R[s][1] = paras[2][0] - paras[2][1] * (s - n - 1)
            R[s + 2 * n][1] = paras[2][0] - paras[2][1] * (s - n - 1) + paras[4]
        
        return (S, A, T, R)
    satr = _parkingMDP(n, paras1)
    writeRes("parking_mdp1.txt",satr)
    satr = _parkingMDP(n, paras2)
    writeRes("parking_mdp2.txt",satr)

    #print(T)

def writeRes(filename, satr):
    mdp = open(filename, 'w')
    S, A, T, R = satr
    mdp.write(str(S) + " " + str(A))
    mdp.write("\n\n")
    for a in T:
        for i in a:
            for j in i:
                mdp.write("%.4f " % j)
            mdp.write("\n")
        mdp.write("\n")
    for s in range(S):
        for a in range(A):
            mdp.write("%.4f " % R[s][a])
        mdp.write("\n")
    mdp.close()


'''
1. Occupation decreasing value 1 / (n - 1), from the closer to the farther.
2. Occupation posibility of Handicap
3. Parking reward, starting from 100, decreasing 100 / (n - 1) each spot which is farther
4. Driving cost
5, Collision Cost
6, Handicap paking reward or cost
'''
n = 10
paras1 = (1 / (n - 0.5), 0.01, (1000, 1000 / (n - 1)), -10, -100, -100)
paras2 = (1 / (n - 0.5), 0.01, (1000, 1000 / (n - 1)), -10, -20000, -100)
parkingMDP(n, paras1, paras2)
