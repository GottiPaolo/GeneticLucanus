from Lucani import *
import matplotlib.pyplot as plt

def save_best_brain():
    best_lucano = min(lucani, key=lambda l: l.fitness)
    NN.save_brain_to_file(best_lucano.brain, f"Salvataggi/best_{gen_count}_{neural_net_shape}_{round(best_lucano.fitness,2)}.txt")

            

 
## Parametri
population_size = 100
to_save = 3
to_rep = 20
to_death = population_size - to_rep
mutation_rate = 0.01
gen_time = 300
gen_count = 0
n_piante = 1
running = True
show = False
graph = True
finestra = (1200,700)
neural_net_shape =  [2,3,3,4]

fitness_minimo  = []
fitness_medio   = []
fitness_massimo = []
##
            
            
# Configura la figura
if graph:
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
    global lucani, piante, gen_count, fitness_minimo, fitness_medio, fitness_massimo
    lucani = sorted(lucani, key = lambda l: -l.fitness)
    if gen_count > 150:
        with open("temp.txt",'w') as file:
            file.write(f'minimo: {fitness_minimo}\n')
            file.write(f'medio: {fitness_medio}\n')
            file.write(f'massimo: {fitness_massimo}\n')
        save_best_brain()
        quit()
    temp = [l.fitness for l in lucani]
    print('Generazione',gen_count)
    print('Media scarti',np.mean(temp[:to_death]), len(temp[:to_death]))
    print('Media genitori',np.mean(temp[-to_rep:]), len(temp[-to_rep:]))
    print('Media elite',np.mean(temp[-to_save:]), len(temp[-to_save:]))   
    print('\tNumero piante rimanenti',len(piante))
    print('\tFitness minimo',temp[-1])
    print('\tFitness medio',np.mean(temp))
    print('\tFitness massimo',temp[0])
    fitness_minimo.append(temp[-1])
    fitness_medio.append(float(np.mean(temp)))
    fitness_massimo.append(temp[0])
    

    for i in range(to_death):
        padre_index = -np.random.randint(1,to_rep)
        madre_index = -np.random.randint(1,to_rep)
        padre = lucani[padre_index]
        madre = lucani[madre_index]

        del lucani[i].brain
        lucani[i].brain = padre.brain.mix(madre.brain,mutation_rate)

    
 
    for p in lucani:
        p.reset()
                
def aggiorna_piante():
    global piante
    piante = [gg.Vector2(np.random.random()*1200, np.random.random()*700) for k in range(n_piante)]
    

    
gg.init()
if show:
    screen = gg.display.set_mode((1200, 700))
    gg.display.set_caption("Davide Simulation")
    clock = gg.time.Clock()
    lucano_image = gg.image.load("img/lucano.png")
    lucano_image = gg.transform.scale(lucano_image, (30, 50))  # Resize the image to 30x50 pixels
    
    
    lucano_image_best = gg.image.load("img/lucano2.png")
    lucano_image_best = gg.transform.scale(lucano_image, (30, 50))  # Resize the image to 30x50 pixels
    
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
            if i != 0:
                rotated_image = gg.transform.rotate(lucano_image, 270)
                rotated_image = gg.transform.rotate(rotated_image, lucano.dir.angle_to(gg.Vector2(1,0)))
                # Center the image on the Lucano's position
                image_rect = rotated_image.get_rect(center=(lucano.p.x, lucano.p.y))
                screen.blit(rotated_image, image_rect.topleft)
            else:
                rotated_image_best = gg.transform.rotate(lucano_image_best, 270)
                rotated_image_best = gg.transform.rotate(rotated_image_best, lucano.dir.angle_to(gg.Vector2(1,0)))
                # Center the image on the Lucano's position
                image_rect = rotated_image_best.get_rect(center=(lucano.p.x, lucano.p.y))
                screen.blit(rotated_image_best, image_rect.topleft)
        

        d_min=np.inf
        for index,(x,y) in enumerate(piante):
            distanza = lucano.p.distance_to(gg.Vector2(x, y))
            if distanza < d_min:
                d_min = distanza
                pianta_vicina = index
            if distanza < 5:
                pass 
                #piante.remove(gg.Vector2(x, y))
                #piante.append(gg.Vector2(np.random.random()*1200, np.random.random()*700))
                # lucano.stamina = min(lucano.stamina + 200, lucano.max_stamina)

        angolo_pianta_vicina = lucano.dir.angle_to( piante[pianta_vicina] - lucano.p)
        if abs(angolo_pianta_vicina) > 180:
            #print('pre',angolo_pianta_vicina)
            angolo_pianta_vicina = 360 - angolo_pianta_vicina* abs(angolo_pianta_vicina) / angolo_pianta_vicina
            #print('pos',angolo_pianta_vicina)
           
        angolo_pianta_vicina /= 180
        
        lucano.ragiona(angolo_pianta_vicina,d_min * 1.5 /min(finestra))
        #lucano.fitness -= d_min
        lucano.fitness += d_min
        # lucano.fitness -= 0.3 * lucano.p.distance_to(gg.Vector2(finestra[0]//2,finestra[1]//2)) 
        
    if frame_ % gen_time == 0:

        # for lucano in lucani:
        #     #lucano.fitness = min([lucano.p.distance_to(p) for p in piante])
        #     lucano.fitness /= gen_time
        gen_count += 1
        new_gen()
        aggiorna_piante()
        if fitness_minimo[-1] < 50 and False:
            save_best_brain()
            print(f"SALVATAGGIO - {gen_count} - {round(fitness_minimo[-1],2)}")
            pass
        
        if gen_count == 800:
            gen_time = 500        
        elif gen_count == 1500:
            gen_time = 1000
        elif gen_count > 2000:
            gen_time = np.random.choice([100,500,1000,2000,5000])
        #if gen_count % 10 == 0:
        #    n_piante -= 10
        if gen_count%20 == 0 and graph:
            update_plot()
        
        

        

    
    if show and frame_ % 10 == 0:
        gg.display.flip()
        clock.tick(60)


