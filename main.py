from Lucani import *
import matplotlib.pyplot as plt

def save_best_brain():
    best_lucano = max(lucani, key=lambda l: l.fitness)
    NN.save_brain_to_file(best_lucano.brain, f"Salvataggi/best_{gen_count}_{neural_net_shape}_{round(best_lucano.fitness,2)}.txt")

            

 
## Parametri
population_size = 300
to_save = population_size // 30
to_rep = population_size // 2
mutation_rate = 0.01
gen_time = 50
gen_count = 0
n_piante = 1
running = True
show = True
finestra = (1200,700)
neural_net_shape =  [4,3,3,4]

fitness_minimo  = []
fitness_medio   = []
fitness_massimo = []
##
            
            
# Configura la figura
plt.ion()  # Modalità interattiva
fig, ax = plt.subplots()
line_min, = ax.plot(range(gen_count), fitness_minimo, label='Fitness Minimo')
line_max, = ax.plot(range(gen_count), fitness_massimo, label='Fitness Massimo')
line_med, = ax.plot(range(gen_count), fitness_medio, label='Fitness Medio')

ax.set_title("Evoluzione del Fitness")
ax.set_xlabel("Generazioni")
ax.set_ylabel("Fitness")
ax.legend()
ax.grid()

# Funzione per aggiornare il grafico
def update_plot():
    global gen_count, fitness_minimo, fitness_medio, fitness_massimo

    # Aggiorna i dati delle linee
    line_min.set_data(range(gen_count), fitness_minimo)
    line_max.set_data(range(gen_count), fitness_massimo)
    line_med.set_data(range(gen_count), fitness_medio)

    # Aggiorna limiti degli assi
    ax.set_xlim(0, gen_count)
    ax.set_ylim(min(fitness_minimo) - 0.5, max(fitness_massimo) + 0.5)

    # Ridisegna la figura
    plt.draw()
    plt.pause(0.1)
            
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
    

    
gg.init()
if show:
    screen = gg.display.set_mode((1200, 700))
    gg.display.set_caption("Davide Simulation")
    clock = gg.time.Clock()
    lucano_image = gg.image.load("img/lucano.png")
    lucano_image = gg.transform.scale(lucano_image, (30, 50))  # Resize the image to 30x50 pixels
    
lucani = [Lucano(finestra[0]//2, finestra[1]//2,neural_net_shape) for i in range(population_size)]
piante = [gg.Vector2(np.random.random()*1200, np.random.random()*700) for k in range(n_piante)]
#lucano = Lucano(400, 300)


frame_ = 0
while running:
    frame_+=1  
    for event in gg.event.get():
        if event.type == gg.QUIT:
            gg.quit()
        elif event.type == gg.KEYDOWN:
            if event.key == gg.K_s:  # Press 's' to save the best brain
                save_best_brain()
    if show:
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
        #  lucano.stamina -= 5
        # lucano.fitness += lucano.stamina # funzione di fitness troppo complessa, da utilizzare più avanti
        
        d_min=1_000
        v = None
        for x,y in piante:
            distanza = lucano.p.distance_to(gg.Vector2(x, y))
            if distanza < d_min:
                d_min = distanza
                v = (x,y)
            if distanza < 5:
                pass 
                #piante.remove(gg.Vector2(x, y))
                #piante.append(gg.Vector2(np.random.random()*1200, np.random.random()*700))
                # lucano.stamina = min(lucano.stamina + 200, lucano.max_stamina)
        if v:
            angolo_pianta_vicina = lucano.p.angle_to(gg.Vector2(*v)) / 180
        else:
            angolo_pianta_vicina = 0
        lucano.ragiona(angolo_pianta_vicina)
        #lucano.fitness -= d_min

    if frame_ % gen_time == 0:
        for l in lucani:
            print(l.fitness)
            l.fitness = -min([l.p.distance_to(p) for p in piante])
        gen_count += 1
        print('Generazione',gen_count)
        print('\tNumero piante rimanenti',len(piante))
        print('\tFitness minimo',np.min([l.fitness for l in lucani]))
        print('\tFitness medio',np.mean([l.fitness for l in lucani]))
        print('\tFitness massimo',np.max([l.fitness for l in lucani]))
        fitness_minimo.append(np.min([l.fitness for l in lucani]))
        fitness_medio.append(np.mean([l.fitness for l in lucani]))
        fitness_massimo.append(np.max([l.fitness for l in lucani]))
        
        if gen_count == 30:
            gen_time = 200        
        elif gen_count == 60:
            gen_time = 300
        elif gen_count > 200:
            gen_time = np.random.choice([100,300,300,300,500,500,500,1000])
        #if gen_count % 10 == 0:
        #    n_piante -= 10
        update_plot()
        
        
        new_gen()
        

    
    if show and frame_ % 10 == 0:
        gg.display.flip()
        clock.tick(60)


