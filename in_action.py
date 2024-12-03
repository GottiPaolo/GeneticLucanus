from Lucani import *
def aggiorna_piante():
    global piante
    piante = [gg.Vector2(np.random.random()*1200, np.random.random()*700) for k in range(n_piante)]
    
 

nice_results = [
    "Salvataggi/best_151_[2, 3, 3, 4]_56.69.txt"
]

## Parametri
n_piante = 1
gen_time = 500
finestra = (1200,700)
neural_net_shape =  [2,3,3,4]
running = True
##
            

    
gg.init()

screen = gg.display.set_mode((1200, 700))
gg.display.set_caption("Davide Simulation")
clock = gg.time.Clock()
lucano_image = gg.image.load("img/lucano.png")
lucano_image = gg.transform.scale(lucano_image, (30, 50))  # Resize the image to 30x50 pixels
    

lucani = [Lucano(finestra[0]//2, finestra[1]//2,neural_net_shape) for i in nice_results]
for lucano,file in zip(lucani,nice_results):
    lucano.br = NN.load_brain_from_file(file)
    
piante = [gg.Vector2(np.random.random()*1200, np.random.random()*700) for k in range(n_piante)]
#lucano = Lucano(400, 300)



frame_ = 0
while running:
    frame_+=1  
    for event in gg.event.get():
        if event.type == gg.QUIT:
            gg.quit()
            
            



    mouse_x, mouse_y = gg.mouse.get_pos()
    piante[0] = gg.Vector2(mouse_x, mouse_y)
    screen.fill((20, 105, 12))
    for x,y in piante:
        gg.draw.circle(screen, (0, 255, 0), (int(x), int(y)), 3)
        
    for i,lucano in enumerate(lucani):

        rotated_image = gg.transform.rotate(lucano_image, 270)
        rotated_image = gg.transform.rotate(rotated_image, lucano.dir.angle_to(gg.Vector2(1,0)))
        # Center the image on the Lucano's position
        image_rect = rotated_image.get_rect(center=(lucano.p.x, lucano.p.y))
        screen.blit(rotated_image, image_rect.topleft)

        d_min=np.inf
        for index,(x,y) in enumerate(piante):
            distanza = lucano.p.distance_to(gg.Vector2(x, y))
            if distanza < d_min:
                d_min = distanza
                pianta_vicina = index
            if distanza < 5:
                pass 
        angolo_pianta_vicina = lucano.dir.angle_to(piante[pianta_vicina] - lucano.p)
    
        
        if abs(angolo_pianta_vicina) > 180:
            angolo_pianta_vicina = 360 - angolo_pianta_vicina* abs(angolo_pianta_vicina) / angolo_pianta_vicina
 
           
        angolo_pianta_vicina /= 180

        lucano.ragiona(angolo_pianta_vicina,d_min * 1.5 /min(finestra))

    if frame_ % gen_time == 0:
        aggiorna_piante()
        lucani[0].reset()
    if frame_ % 1 == 0:
        gg.display.flip()
        clock.tick(60)


