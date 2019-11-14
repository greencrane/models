import numpy as np 

def generateNewArray(N):
    X = np.zeros(N)
    for i in range(N):
        X[i+1] = X[i] + np.random().normal(0,1)
    return X 

print(generateNewArray(10))