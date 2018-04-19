import sys
H = 10
outputV = {(-1, -1): 0}
outputP = {(-1, -1): 0}
def getMDPSATR(filename):
    '''S, A, T, R'''
    MDPFile = open(filename,encoding='utf-8')

    try:
        # first part
        eachline = MDPFile.readline()
        eachline = eachline.replace('\ufeff', '')
        S, A = eachline.split(' ')
        S = int(S)
        A = int(A)
        T = []

        #second part
        T = []
        for i in range(A):
            eachline = MDPFile.readline()
            T.append([])
            for j in range(S):
                T[i].append([])
                eachline = MDPFile.readline()
                data = eachline.split()
                for k in range(S):
                    T[i][j].append(float(data[k]))
                    #print(T)
        #third part
        eachline = MDPFile.readline()
        R = []
        for i in range(S):
            R.append([])
            eachline = MDPFile.readline()
            data = eachline.split()
            for j in range(A):
                R[i].append(float(data[j]))
    finally:
        MDPFile.close()

        return (S,A,T,R)
 #       return roomMap
def main(filename):
    satr = getMDPSATR(filename)
    S, A, T, R = satr
 #   print(R)
 #   print(satr)
    for s in range(S):
        for h in range(H):
            outputV[s,h] = evaluationFun(s, h, satr)
    print("Value Function:")
    for i in range(S):
        for j in range(H)[::-1]:
            print("%.4f" % outputV[i,j],end='')
            print("\t",end='')
        print("")
        
    print("\nPolicy Function:")
    for i in range(S):
        for j in range(H)[::-1]:
            if outputP[i,j] is None:
                print("None",end='')
            else:
                print("%d" % int(outputP[i,j]),end='')
            print("\t",end='')
        print("")
    
    

def evaluationFun(s,h,satr):
    if h == -1:
        outputV[s,h] = 0
        outputP[s,h] = None
        return outputV[s,h]
    if (s,h) in outputV:
        return outputV[s,h]
    
    S, A, T, R = satr
    sv = []
    '''
    action = policyFun(s,h, satr)
    if action is None:
        outputV[s,h] = 0
        return outputV[s,h]
    '''
    maxV = float('-inf')
    maxA = -1
    for a in range(A):
        reward = R[s][a]
        expectedFutrue = 0
        for sp, pr in enumerate(T[a][s]):
            if pr != 0:
                expectedFutrue += pr * evaluationFun(sp, h - 1, satr)
        value = reward + expectedFutrue
        if value > maxV:
            maxV = value
            maxA = a
    if maxA == -1:
        outputP[s,h] = None
        outputV[s,h] = 0
    else:
        outputP[s,h] = maxA
        outputV[s,h] = maxV
    
    return outputV[s,h]
    
    
'''
def policyFun(s,h,satr):
    return 0
'''
    
if __name__=='__main__':
    main("20testcase.txt")
