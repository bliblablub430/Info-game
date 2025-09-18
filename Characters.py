import pygame
import ostblock
import mapinteraction
import Pixel_Währung_und_Sammlung
import herz_system
import sprites
import random

pygame.init()
pygame.display.set_caption("Frau_Weidman_Hunter69")
clock = pygame.time.Clock()

farben = ["R", "Gr", "B", "G", "P"]  # Farbe pro Pixeltyp 
aktuelle_farbe = 0

# Player sprite
x, y = 960, 540
h, l = 40, 50
speed = 10
renzodef = "Renzo\Renzo_1.png"
character = sprites.Sprites(renzodef, pygame.Rect(x, y, h, l))

# NPC sprite(s)
#Frau Weidmann
xw, yw = 800, 600
hw, lw = 40, 50
stepsw = 0
npcspeedw = 20
frau_weidmann = sprites.Sprites("Vampir\Silke_1.png", pygame.Rect(xw, yw, hw, lw))
#Pharao
xp, yp = 100, 800
hp, lp = 40, 50
stepsp = 350
npcspeedp = 20
pharao = sprites.Sprites("Pharao\Pharao_1.png", pygame.Rect(xp, yp, hp, lp))
#alle npcs
npcs = [frau_weidmann, pharao]

pixles = []
pixles_R = []
pixles_Gr = []
pixles_B = []
pixles_G = []
pixles_P = []

def movement(x, y, speed, sprint_unlocked): #actuall movement happens in mapinteraction.wallinteraction
    keys = pygame.key.get_pressed()
    if sprint_unlocked:
        if keys[pygame.K_RSHIFT]:
            speedc = speed*2
        else:
            speedc = speed
    else:
        speedc = speed
    dx, dy = get_movement_vector() 
    x += dx * speedc
    if __name__ == "__main__":
        character.rect.x = x
    y += dy * speedc
    if __name__ == "__main__":
        character.rect.y = y
    return x, y, (dx*speedc), (dy*speedc)

def get_movement_vector():
    dx, dy = 0, 0  # Start with no movement
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_d]:
        dx -= 1
    if keys[pygame.K_a]:
        dx += 1
    if keys[pygame.K_w]:
        dy += 1
    if keys[pygame.K_s]:
        dy -= 1
        

    # Normalize the vector (so diagonal movement isn't faster)
    if dx != 0 or dy != 0:
        vector_len = (dx**2 + dy**2)**0.5
        dx = dx / vector_len
        dy = dy / vector_len
        
    return dx, dy # Return the calculated direction

def npcmovement(npcs, stepsw, npcspeedw, stepsp, npcspeedp):
    xw, yw = frau_weidmann.rect.x, frau_weidmann.rect.y
    xp, yp = pharao.rect.x, pharao.rect.y
    for npc in npcs:
        if npc == frau_weidmann:
            # npc läuft Rechteck ab (algorythmus von Ben)
            if stepsw < 250:
                npc.rect.x -= npcspeedw # nach links
                xw = npc.rect.x  
                yw = npc.rect.y
            elif stepsw < 700:
                npc.rect.y += npcspeedw  # nach unten
                xw = npc.rect.x  
                yw = npc.rect.y
            elif stepsw < 1000:
                npc.rect.x += npcspeedw  # nach rechts
                xw = npc.rect.x  
                yw = npc.rect.y
            elif stepsw < 1200:
                npc.rect.y -= npcspeedw  # nach oben
                xw = npc.rect.x  
                yw = npc.rect.y
            elif stepsw < 1600:
                npc.rect.x -= npcspeedw  # nach links
                xw = npc.rect.x  
                yw = npc.rect.y
            elif stepsw < 2000:
                npc.rect.y += npcspeedw  #nach unten
                xw = npc.rect.x  
                yw = npc.rect.y
            elif stepsw < 2200:
                npc.rect.y -= npcspeedw  #nach oben
                xw = npc.rect.x  
                yw = npc.rect.y
            elif stepsw < 2550:
                npc.rect.x += npcspeedw  #nach rechts
                xw = npc.rect.x  
                yw = npc.rect.y
            elif stepsw < 3000:
                npc.rect.y -= npcspeedw  #nach oben
                xw = npc.rect.x  
                yw = npc.rect.y
            elif stepsw >= 3000:
                stepsw = 0
            stepsw += 1
        elif npc == pharao:
            # npc läuft Dreieck ab
            if stepsp < 500:
                npc.rect.x += npcspeedp  # nach rechts
                xp = npc.rect.x
                yp = npc.rect.y
            elif stepsp < 1000:
                npc.rect.y += npcspeedp  # nach unten
                xp = npc.rect.x
                yp = npc.rect.y
            elif stepsp < 1500:
                npc.rect.x -= npcspeedp  # nach links
                xp = npc.rect.x
                yp = npc.rect.y
            elif stepsp < 2000:
                npc.rect.y += npcspeedp  # nach unten
                xp = npc.rect.x
                yp = npc.rect.y
            elif stepsp < 2500:
                npc.rect.x -= npcspeedp  # nach links
                xp = npc.rect.x
                yp = npc.rect.y
            elif stepsp < 3000:
                npc.rect.y -= npcspeedp  # nach oben
                xp = npc.rect.x
                yp = npc.rect.y
            elif stepsp < 3500:
                npc.rect.y += npcspeedp  # nach unten  
                xp = npc.rect.x
                yp = npc.rect.y
            if stepsp >= 3500:
                stepsp = 0
            stepsp += 1
    return stepsw, stepsp, xw, yw, xp, yp
         
def npcinteraction(lives, last_interaction):
    current_time = pygame.time.get_ticks()
    npc_coolown = 1000
    for npc in npcs:
        if character.rect.colliderect(npc.rect) and current_time - last_interaction > npc_coolown:
            lives = herz_system.lose_life(lives)
            Pixel_Währung_und_Sammlung.PixelBank.add(Pixel_Währung_und_Sammlung.wallet, 5000)
            last_interaction = current_time
    return lives, last_interaction



def drawing(screen, character, npcs, pixles, last_pixel, last_renzo, stepsw, stepsp, xw, yw, xp, yp):
    #check for drawing a pixel
    current_time = pygame.time.get_ticks()
    pixel_coolown = 105
    keys = pygame.key.get_pressed()
    global aktuelle_farbe

    if keys[pygame.K_TAB]:
        aktuelle_farbe = (aktuelle_farbe + 1) % len(farben)

    if keys[pygame.K_j] and current_time - last_pixel > pixel_coolown:
        pixle = draw(character.rect.x, character.rect.y)
        if pixle is not None:
            if farben[aktuelle_farbe] == "R":
                pixles_R.append(pixle)
            elif farben[aktuelle_farbe] == "Gr":
                pixles_Gr.append(pixle)
            elif farben[aktuelle_farbe] == "B":
                pixles_B.append(pixle)
            elif farben[aktuelle_farbe] == "G":
                pixles_G.append(pixle)
            elif farben[aktuelle_farbe] == "P":
                pixles_P.append(pixle)
            else:
                pixles.append(pixle)

            last_pixel = current_time
    #Drawing everything
    ostblock.walldraw(screen) #Draw wall
    dx, dy = get_movement_vector()
    renzo = ["Renzo\Renzo_1.png", "Renzo\Renzo_2.png", "Renzo\Renzo_3.png", "Renzo\Renzo_4.png", "Renzo\Renzo_5.png", "Renzo\Renzo_6.png", "Renzo\Renzo_7.png", "Renzo\Renzo_8.png", "Renzo\Renzo_9.png", "Renzo\Renzo_10.png", "Renzo\Renzo_11.png", "Renzo\Renzo_12.png", ]
    if dy < 0:
        renzodef = random.choice(renzo[0:3])
        character = sprites.Sprites(renzodef, pygame.Rect(x, y, h, l))
        screen.blit(character.image, character.rect) # Draw player sprite
        last_renzo = renzodef
    elif dy > 0:
        renzodef = random.choice(renzo[3:6])
        character = sprites.Sprites(renzodef, pygame.Rect(x, y, h, l))
        screen.blit(character.image, character.rect) # Draw player sprite
        last_renzo = renzodef
    elif dx < 0:
        renzodef = random.choice(renzo[6:9])
        character = sprites.Sprites(renzodef, pygame.Rect(x, y, h, l))
        screen.blit(character.image, character.rect) # Draw player sprite
        last_renzo = renzodef
    elif dx > 0:
        renzodef = random.choice(renzo[9:12])
        character = sprites.Sprites(renzodef, pygame.Rect(x, y, h, l))
        screen.blit(character.image, character.rect) # Draw player sprite
        last_renzo = renzodef
    else:
        character = sprites.Sprites(last_renzo, pygame.Rect(x, y, h, l))
        screen.blit(character.image, character.rect) # Draw player sprite
    # npc animation
    silke = ["Vampir\Silke_1.png", "Vampir\Silke_2.png", "Vampir\Silke_3.png", "Vampir\Silke_4.png", "Vampir\Silke_5.png", "Vampir\Silke_6.png", "Vampir\Silke_7.png", "Vampir\Silke_8.png", ]
    if stepsw < 250:
        if stepsw % 5 == 0: #alle fünf frames
            frau_weidmann = sprites.Sprites(silke[2], pygame.Rect(xw, yw, hw, lw))
            screen.blit(frau_weidmann.image, frau_weidmann.rect)
        else:
            frau_weidmann = sprites.Sprites(silke[3], pygame.Rect(xw, yw, hw, lw))
            screen.blit(frau_weidmann.image, frau_weidmann.rect) # nach links
    elif stepsw < 700:
        if stepsw % 5 == 0:
            frau_weidmann = sprites.Sprites(silke[0], pygame.Rect(xw, yw, hw, lw))
            screen.blit(frau_weidmann.image, frau_weidmann.rect) # Draw NPC sprite(s)
        else:
            frau_weidmann = sprites.Sprites(silke[1], pygame.Rect(xw, yw, hw, lw))
            screen.blit(frau_weidmann.image, frau_weidmann.rect) # nach unten
    elif stepsw < 1000:
        if stepsw % 5 == 0:
            frau_weidmann = sprites.Sprites(silke[4], pygame.Rect(xw, yw, hw, lw))
            screen.blit(frau_weidmann.image, frau_weidmann.rect) # Draw NPC sprite(s)
        else:
            frau_weidmann = sprites.Sprites(silke[5], pygame.Rect(xw, yw, hw, lw))
            screen.blit(frau_weidmann.image, frau_weidmann.rect) # nach rechts
    elif stepsw < 1200:
        if stepsw % 5 == 0:
            frau_weidmann = sprites.Sprites(silke[6], pygame.Rect(xw, yw, hw, lw))
            screen.blit(frau_weidmann.image, frau_weidmann.rect) # Draw NPC sprite(s)
        else:
            frau_weidmann = sprites.Sprites(silke[7], pygame.Rect(xw, yw, hw, lw))
            screen.blit(frau_weidmann.image, frau_weidmann.rect) # nach oben
    elif stepsw < 1600:
        if stepsw % 5 == 0:
            frau_weidmann = sprites.Sprites(silke[2], pygame.Rect(xw, yw, hw, lw))
            screen.blit(frau_weidmann.image, frau_weidmann.rect) # Draw NPC sprite(s)
        else:
            frau_weidmann = sprites.Sprites(silke[3], pygame.Rect(xw, yw, hw, lw))
            screen.blit(frau_weidmann.image, frau_weidmann.rect)  # nach links
    elif stepsw < 2000:
        if stepsw % 5 == 0:
            frau_weidmann = sprites.Sprites(silke[0], pygame.Rect(xw, yw, hw, lw))
            screen.blit(frau_weidmann.image, frau_weidmann.rect) # Draw NPC sprite(s)
        else:
            frau_weidmann = sprites.Sprites(silke[1], pygame.Rect(xw, yw, hw, lw))
            screen.blit(frau_weidmann.image, frau_weidmann.rect)  #nach unten
    elif stepsw < 2200:
        if stepsw % 5 == 0:
            frau_weidmann = sprites.Sprites(silke[6], pygame.Rect(xw, yw, hw, lw))
            screen.blit(frau_weidmann.image, frau_weidmann.rect) # Draw NPC sprite(s)
        else:
            frau_weidmann = sprites.Sprites(silke[7], pygame.Rect(xw, yw, hw, lw))
            screen.blit(frau_weidmann.image, frau_weidmann.rect)  #nach oben
    elif stepsw < 2550:
        if stepsw % 5 == 0:
            frau_weidmann = sprites.Sprites(silke[4], pygame.Rect(xw, yw, hw, lw))
            screen.blit(frau_weidmann.image, frau_weidmann.rect) # Draw NPC sprite(s)
        else:
            frau_weidmann = sprites.Sprites(silke[5], pygame.Rect(xw, yw, hw, lw))
            screen.blit(frau_weidmann.image, frau_weidmann.rect)  #nach rechts
    elif stepsw < 3000:
        if stepsw % 5 == 0:
            frau_weidmann = sprites.Sprites(silke[6], pygame.Rect(xw, yw, hw, lw))
            screen.blit(frau_weidmann.image, frau_weidmann.rect) # Draw NPC sprite(s)
        else:
            frau_weidmann = sprites.Sprites(silke[7], pygame.Rect(xw, yw, hw, lw))
            screen.blit(frau_weidmann.image, frau_weidmann.rect)  #nach oben
    elif stepsw >= 3000:
        stepsw = 0
    stepsw += 1
    #pharao
    zady = ["Pharao\Pharao_1.png", "Pharao\Pharao_2.png", "Pharao\Pharao_3.png", "Pharao\Pharao_4.png", "Pharao\Pharao_5.png", "Pharao\Pharao_6.png", "Pharao\Pharao_7.png", "Pharao\Pharao_8.png", "Pharao\Pharao_9.png", "Pharao\Pharao_10.png", ]
    if stepsp < 500:
        if stepsp % 5 == 0: #alle fünf frames
            pharao = sprites.Sprites(zady[8], pygame.Rect(xp, yp, hp, lp))
            screen.blit(pharao.image, pharao.rect)
        else:
            pharao = sprites.Sprites(zady[9], pygame.Rect(xp, yp, hp, lp))
            screen.blit(pharao.image, pharao.rect) #nach rechts
    elif stepsp < 1000:
        if stepsp % 5 == 0: #alle fünf frames
            pharao = sprites.Sprites(zady[3], pygame.Rect(xp, yp, hp, lp))
            screen.blit(pharao.image, pharao.rect)
        elif stepsp % 3 == 0:
            pharao = sprites.Sprites(zady[4], pygame.Rect(xp, yp, hp, lp))
            screen.blit(pharao.image, pharao.rect)
        else:
            pharao = sprites.Sprites(zady[5], pygame.Rect(xp, yp, hp, lp))
            screen.blit(pharao.image, pharao.rect) #nach unten
    elif stepsp < 1500:
        if stepsp % 5 == 0: #alle fünf frames
            pharao = sprites.Sprites(zady[6], pygame.Rect(xp, yp, hp, lp))
            screen.blit(pharao.image, pharao.rect)
        else:
            pharao = sprites.Sprites(zady[7], pygame.Rect(xp, yp, hp, lp))
            screen.blit(pharao.image, pharao.rect) #nach links
    elif stepsp < 2000:
        if stepsp % 5 == 0: #alle fünf frames
            pharao = sprites.Sprites(zady[3], pygame.Rect(xp, yp, hp, lp))
            screen.blit(pharao.image, pharao.rect)
        elif stepsp % 3 == 0:
            pharao = sprites.Sprites(zady[4], pygame.Rect(xp, yp, hp, lp))
            screen.blit(pharao.image, pharao.rect)
        else:
            pharao = sprites.Sprites(zady[5], pygame.Rect(xp, yp, hp, lp))
            screen.blit(pharao.image, pharao.rect) #nach unten
    elif stepsp < 2500:
        if stepsp % 5 == 0: #alle fünf frames
            pharao = sprites.Sprites(zady[6], pygame.Rect(xp, yp, hp, lp))
            screen.blit(pharao.image, pharao.rect) #nach links
        else:
            pharao = sprites.Sprites(zady[7], pygame.Rect(xp, yp, hp, lp))
            screen.blit(pharao.image, pharao.rect)
    elif stepsp < 3000:
        if stepsp % 5 == 0: #alle fünf frames
            pharao = sprites.Sprites(zady[0], pygame.Rect(xp, yp, hp, lp))
            screen.blit(pharao.image, pharao.rect)
        elif stepsp % 3 == 0:
            pharao = sprites.Sprites(zady[1], pygame.Rect(xp, yp, hp, lp))
            screen.blit(pharao.image, pharao.rect)
        else:
            pharao = sprites.Sprites(zady[2], pygame.Rect(xp, yp, hp, lp))
            screen.blit(pharao.image, pharao.rect) #nach oben
    elif stepsp < 3500:
        if stepsp % 5 == 0: #alle fünf frames
            pharao = sprites.Sprites(zady[3], pygame.Rect(xp, yp, hp, lp))
            screen.blit(pharao.image, pharao.rect)
        elif stepsp % 3 == 0:
            pharao = sprites.Sprites(zady[4], pygame.Rect(xp, yp, hp, lp))
            screen.blit(pharao.image, pharao.rect)
        else:
            pharao = sprites.Sprites(zady[5], pygame.Rect(xp, yp, hp, lp))
            screen.blit(pharao.image, pharao.rect) #nach unten
    if stepsp >= 3500:
        stepsp = 0
    stepsp += 1    


    for p in pixles_R:
        pygame.draw.rect(screen, (250, 0, 0), p)

    for p in pixles_Gr:
        pygame.draw.rect(screen, (0, 250, 0), p)

    for p in pixles_B:
        pygame.draw.rect(screen, (0, 0, 250), p)

    for p in pixles_G:
        pygame.draw.rect(screen, (255, 255, 0), p)

    for p in pixles_P:
        pygame.draw.rect(screen, (255, 51, 255), p)

    for p in pixles:
        pygame.draw.rect(screen, (0, 255, 0), p)

    return last_pixel, last_renzo, stepsw, stepsp


def draw(x,y):
    if Pixel_Währung_und_Sammlung.wallet.can_spend(1):
        pixle = pygame.Rect(x, y, 50, 50)
        mapinteraction.add_to_almosteverything(pixle, mapinteraction.almosteverything)
        Pixel_Währung_und_Sammlung.wallet.spend(1)
        return pixle

if __name__ == "__main__": #used in the begining for checking the file on its own (no longer works)

    screen = pygame.display.set_mode((1920, 1080))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        x, y, dx, dy = movement(x, y, speed)
        steps = npcmovement(npcs, steps, npcspeed)
        screen.fill((0, 0, 0)) # Clear screen
        drawing(screen, character, npcs, pixles)
        pygame.display.update() # Update the display
        clock.tick(60)

    pygame.quit() # Quit pygame properly
