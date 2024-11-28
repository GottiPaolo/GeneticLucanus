
from Lucani import *
from parametri import *

## Parametri
population_size = 100
to_save = population_size // 20
to_rep = population_size // 3
mutation_rate = 0.02
gen_time = 100
gen_count = 0
n_piante = 200
running = True
show = True
##         
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
        
def resetpiante():
    global piante
    piante = [gg.Vector2(np.random.random()*1200, np.random.random()*700) for k in range(n_piante)]
    

        

gg.init()
if show:
    screen = gg.display.set_mode((1200, 700))
    gg.display.set_caption("Davide Simulation")
    clock = gg.time.Clock()
    lucano_image = gg.image.load("img/lucano.png")
    lucano_image = gg.transform.scale(lucano_image, (30, 50))  # Resize the image to 30x50 pixels

lucani = [Lucano(600, 350) for i in range(population_size)]
piante = [gg.Vector2(np.random.random()*1200, np.random.random()*700) for k in range(n_piante)]
#lucano = Lucano(400, 300)


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
        d_min = 1_000
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
        resetpiante()

    
    if show:
        gg.display.flip()
        clock.tick(60)


