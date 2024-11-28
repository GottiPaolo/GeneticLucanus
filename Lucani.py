import pygame as gg
from NeuralNets import *

class Lucano:
    raggio_visivo = 100
    max_stamina = 1000
    Live = True
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
        