import sys
import parking_MDP
from value_iteration import VIfun
from policy_iteration import PIfun
from modified_policy_iteration import MPIfun
from copy import deepcopy
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
epsilon = 0.00001
Beta = {0.1,0.9, 0.999}
def main(filename, isParkingMDP = False):
    satr = getMDPSATR(filename)
    S, A, T, R = satr
    '''
    print(S)
    print(A)
    print(T)
    print(R)
    '''
    file = open(filename[:-4] + "_res.txt",'w')

    file.write("------------------Value Iteration------------------\n")
    resV = []
    resP = []
    for beta in Beta:
        outputV = {}
        outputP = {}
        VIfun(satr, outputV, outputP, beta, epsilon)
        resV.append(deepcopy(outputV))
        resP.append(deepcopy(outputP))
    if isParkingMDP:
        writeParkingRes(file,resV,resP,S)
    else:
        writeRes(file,resV,resP,S)
    
    file.write("\n------------------Policy Iteration------------------\n")
    resV = []
    resP = []

    for beta in Beta:
        outputV = {}
        outputP = {}
        PIfun(satr, outputV, outputP, beta, epsilon)
        resV.append(deepcopy(outputV))
        resP.append(deepcopy(outputP))
    if isParkingMDP:
        writeParkingRes(file,resV,resP,S)
    else:
        writeRes(file,resV,resP,S)
    
    file.write("\n------------------Modified Policy Iteration------------------\n")
    resV = []
    resP = []

    for beta in Beta:
        outputV = {}
        outputP = {}
        MPIfun(satr, outputV, outputP, beta, epsilon)
        resV.append(deepcopy(outputV))
        resP.append(deepcopy(outputP))
    if isParkingMDP:
        writeParkingRes(file,resV,resP,S)
    else:
        writeRes(file,resV,resP,S)
    file.close()
    
    print("Results is saved in " + filename)
    
def printRes(resV,resP,S):
    print("Value Function:")
    for b, beta in enumerate(Beta):
        for i in range(S):
            print("%.4f" % resV[b][i],end='')
            print("\t",end='')
        print("")
    
          
    print("\n\nPolicy Function:")
    for b, beta in enumerate(Beta):
        for i in range(S):
            if resP[beta - 1][i] is None:
                print("None",end='')
            else:
                print("%d" % int(resP[b][i]),end='')
            print("\t",end='')
        print("")

def writeRes(file,resV,resP,S):
    
    file.write("Value Function:\n")
    for b, beta in enumerate(Beta):
        file.write("\nbeta = %4f" % beta + "\n")
        for i in range(S):
            file.write("%.4f" % resV[b][i])
            file.write(" ")
        file.write("\n")
    
          
    file.write("\n\nPolicy Function:\n")
    for b, beta in enumerate(Beta):
        file.write("\nbeta = %4f" % beta + "\n")
        for i in range(S):
            if resP[b][i] is None:
                file.write("None")
            else:
                file.write("%d" % int(resP[b][i]))
            file.write(" ")
        file.write("\n")

def writeParkingRes(file,resV,resP,S):
    
    file.write("Value Function:\n")
    n = 10
    for b, beta in enumerate(Beta):
        file.write("\nbeta = %4f" % beta + "\n")
        for i in range(2):
            for j in range(2 * n):
                if j < 10:
                    resStr = "(A-" + str(n - j) + ", "
                else:
                    resStr = "(B-" + str(j - 10 + 1) + ", "
                if i ==0:
                    resStr += "unoccupied, unparked):"
                else:
                    resStr += "occupied, unparked):"
                file.write(resStr + "%.4f\n" % resV[b][i * 2 * n + j])
        file.write("terminal(-, -, Parked) : 0.0000")
        file.write("\n\n")
    
          
    file.write("\n\nPolicy Function:\n")
    for b, beta in enumerate(Beta):
        file.write("\nbeta = %4f" % beta + "\n")
        for i in range(2):
            for j in range(2 * n):
                if j < 10:
                    resStr = "(A-" + str(n - j) + ", "
                else:
                    resStr = "(B-" + str(j - 10 + 1) + ", "
                if i ==0:
                    resStr += "unoccupied, unparked):"
                else:
                    resStr += "occupied, unparked):"
                if resP[b][i] is None:
                    file.write(resStr + "None")
                else:
                    if resP[b][i * 2 * n + j] == 0:
                        resStr += "Drive"
                    else:
                        resStr += "Park"
                    file.write(resStr + "\n")
        file.write("terminal(-, -, Parked) : None")                
        file.write("\n\n")

        
    
if __name__=='__main__':
    main("MDP1-hw3.txt")
    main("MDP2-hw3.txt")
    main("paking_mdp1.txt", isParkingMDP = True)
    main("paking_mdp2.txt", isParkingMDP = True)
 #   main("output_parking_problem2.txt", isParkingMDP = False)
    
