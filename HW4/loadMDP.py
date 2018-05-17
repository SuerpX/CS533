def loadMDP(filename):
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
