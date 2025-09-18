import Characters
import pygame
npchunter1speed = 5
npchunter1 = pygame.Rect(100, 100, 50, 50)
def npchunter1(npchunter1, character, npchunter1speed):
    #npc algoritmus
    x_vector_npc_character = Characters.character.x - Characters.npc.x
    y_vector_npc_character = Characters.character.y - Characters.npc.y
        # Länge (Distanz) des Vektors berechnen
    dist = (x_vector_npc_character**2 + y_vector_npc_character**2)**0.5

    
    # Normalisiere Vektor (Länge 1)
    x_vector_npc_character /= dist
    y_vector_npc_character /= dist
    # Bewege NPC in Richtung des Charakters
    Characters.npc.x += x_vector_npc_character * npchunter1speed
    Characters.npc.y += y_vector_npc_character * npchunter1speed
npchunter1(npchunter1, Characters.character, 5)