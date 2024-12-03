
import numpy as np 
class NN:
    def __init__(self,layers):
        self.shape = layers
        self.matrices = [np.random.uniform(-1, 1, (layers[i], layers[i+1])) for i in range(len(layers)-1)]  
        self.biases = [np.random.uniform(-1,1, n) for n in layers[1:]] 
        self.activation_f = lambda x: (1-np.e**(-x))/(1+np.e**(-x))  
        
    def esegui(self,input):
        assert len(input) == self.shape[0]
        step = np.array(input)
        for matrice,bias in zip(self.matrices,self.biases):
            step = self.activation_f(np.dot(step, matrice)- bias)
        return step
    
    def mostra(self):
        print(*self.matrices)
        print(*self.biases)
    
    def mix(self,other, mutation_rate):
        assert self.shape == other.shape
        new = NN(self.shape)
        for i in range(len(self.matrices)):
            new.matrices[i] = np.where(np.random.rand(*self.matrices[i].shape) < 0.5, self.matrices[i], other.matrices[i])
            new.biases[i] = np.where(np.random.rand(*self.biases[i].shape) < 0.5, self.biases[i], other.biases[i])
            mutation_mask = np.random.rand(*self.matrices[i].shape) < mutation_rate
            new.matrices[i][mutation_mask] = np.random.uniform(-1, 1, mutation_mask.sum())
            mutation_mask = np.random.rand(*self.biases[i].shape) < mutation_rate
            new.biases[i][mutation_mask] = np.random.uniform(-1, 1, mutation_mask.sum())
        return new
    
    def save_brain_to_file(brain, filename):
        with open(filename, 'w') as f:
            f.write(f"{brain.shape}\n")
            for matrix in brain.matrices:
                np.savetxt(f, matrix)
            for bias in brain.biases:
                np.savetxt(f, bias)

    def load_brain_from_file(filename):
        with open(filename, 'r') as f:
            shape = eval(f.readline().strip())
            matrices = []
            biases = []
            for i in range(len(shape) - 1):
                matrix = np.loadtxt(f, max_rows=shape[i])
                matrices.append(matrix)
            for i in range(1, len(shape)):
                bias = np.loadtxt(f, max_rows=shape[i])
                biases.append(bias)
        brain = NN(shape)
        brain.matrices = matrices
        brain.biases = biases
        return brain
def save_brain_to_file(brain, filename):
    with open(filename, 'w') as f:
        f.write(f"{brain.shape}\n")
        for matrix in brain.matrices:
            for row in matrix:
                for value in row:
                    f.write(f"{value}\n")
        for bias in brain.biases:
            for value in bias:
                f.write(f"{value}\n")

def load_brain_from_file(filename):
    with open(filename, 'r') as f:
        shape = eval(f.readline().strip())
        matrices = []
        biases = []
        for i in range(len(shape) - 1):
            matrix = []
            for _ in range(shape[i]):
                row = [float(f.readline().strip()) for _ in range(shape[i + 1])]
                matrix.append(row)
            matrices.append(np.array(matrix))
        for i in range(1, len(shape)):
            bias = [float(f.readline().strip()) for _ in range(shape[i])]
            biases.append(np.array(bias))
    brain = NN(shape)
    brain.matrices = matrices
    brain.biases = biases
    return brain
 