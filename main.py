import pygame as gg
import numpy as np

class Lucano:
    raggio_visivo = 100
    max_stamina = 1000
    def __init__(self, x,y):
        self.p = gg.Vector2(x, y)
        self.dir = gg.Vector2(1, 0)
        self.brain = NN([4,5,5,4])
        self.stamina = self.max_stamina
        self.vede_pianta = False
        self.fitness = 0

    def muovi(self, velocita):
        if self.stamina > 0:
            movimento = self.dir * velocita
            self.p += movimento
            self.stamina -= abs(velocita*0.1)
            if self.stamina < 0:
                self.fitness = 0

    def ruota_orientamento(self, angolo):
        self.dir = self.dir.rotate(angolo)
        
    def dead(self):
        pass
        #crepa
        
    def ragiona(self,angolo_pianta_vicina):
        input_ = [angolo_pianta_vicina, self.dir.x, self.dir.y , self.stamina/self.max_stamina]
        output = self.brain.esegui(input_)
        energia = (output[3]+1)*3
        angolo =  (output[2]+1)*2
        if output[0] > 0:
            self.muovi(energia)
        if output[1] > 0:
            self.ruota_orientamento(angolo)
        return output
    
    def reset(self):
        self.p = (600, 350)
        self.dir =  gg.Vector2(1, 0)
        self.stamina = self.max_stamina
        self.vede_pianta = False
        self.fitness = 0
        
        
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
          
def new_gen():
    global lucani, piante, population_size
    lucani = sorted(lucani, key = lambda l:l.fitness)
    new_brains = []
    for i in range(population_size-to_save):
        padre = lucani[-np.random.randint(1,to_rep)]
        madre = lucani[-np.random.randint(1,to_rep)]
        new_brains.append(padre.brain.mix(madre.brain,mutation_rate))
    
    for i in range(population_size-to_save):
        lucani[i].brain = new_brains[i]
        
    for p in lucani:
        p.reset()
        p.p = gg.Vector2(600, 350)
        p.dir = gg.Vector2(1, 0)
        
    piante = [gg.Vector2(np.random.random()*1200, np.random.random()*700) for k in range(n_piante)]
    
## Parametri
population_size = 100
to_save = population_size // 10
to_rep = population_size // 3
mutation_rate = 0.01
gen_time = 100
gen_count = 0
n_piante = 400

##
        

gg.init()
screen = gg.display.set_mode((1200, 700))
gg.display.set_caption("Davide Simulation")
clock = gg.time.Clock()

lucano_image = gg.image.load("img/lucano.png")
lucano_image = gg.transform.scale(lucano_image, (30, 50))  # Resize the image to 30x50 pixels
lucani = [Lucano(600, 350) for i in range(population_size)]
piante = [gg.Vector2(np.random.random()*1200, np.random.random()*700) for k in range(n_piante)]
#lucano = Lucano(400, 300)

running = True
show = True
frame_ = 0
while running:
    frame_+=1  

    if show:
        for event in gg.event.get():
            if event.type == gg.QUIT:
                gg.quit()
 
        screen.fill((20, 105, 12))
        for x,y in piante:
            gg.draw.circle(screen, (0, 255, 0), (int(x), int(y)), 3)
        
    for i,lucano in enumerate(lucani):
        if show:
            rotated_image = gg.transform.rotate(lucano_image, 270)
            rotated_image = gg.transform.rotate(rotated_image, lucano.dir.angle_to(gg.Vector2(1,0)))
            # Center the image on the Lucano's position
            image_rect = rotated_image.get_rect(center=(lucano.p.x, lucano.p.y))
            screen.blit(rotated_image, image_rect.topleft)
        lucano.stamina -= 5
        lucano.fitness += lucano.stamina
        d_min=1_000
        v = None
        for x,y in piante:
            distanza = lucano.p.distance_to(gg.Vector2(x, y))
            if distanza < d_min:
                d_min = distanza
                v = (x,y)
            if distanza < 5:
                piante.remove(gg.Vector2(x, y))
                lucano.stamina = min(lucano.stamina + 100, lucano.max_stamina)
        if v:
            angolo_pianta_vicina = lucano.p.angle_to(gg.Vector2(*v)) / 180
        else:
            angolo_pianta_vicina = 0
        lucano.ragiona(angolo_pianta_vicina)

    if frame_ % gen_time == 0:
        gen_count += 1
        print('Generazione',gen_count)
        print('\tNumero piante rimanenti',len(piante))
        print('\tFitness minimo',np.min([l.fitness for l in lucani]))
        print('\tFitness medio',np.mean([l.fitness for l in lucani]))
        print('\tFitness massimo',np.max([l.fitness for l in lucani]))
        if gen_count == 30:
            gen_time = 200        
        if gen_count == 60:
            gen_time = 500
            
        

        new_gen()

    
    if show:
        gg.display.flip()
    clock.tick(60)


