import pygame
import ostblock
import mapinteraction

pygame.init()
pygame.display.set_caption("Frau_Weidman_Hunter69")
clock = pygame.time.Clock()

# Player variables
x, y = 960, 540
h, l = 50, 50
speed = 10
character = pygame.Rect(x, y, h, l)

xn, yn = 800, 600
hn, ln = 50, 50
steps = 0
npcspeed = 5
npc = pygame.Rect(xn, yn, hn, ln)

pixles = []

def movement(x, y, speed): #actuall movement happens in mapinteraction.wallinteraction
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LSHIFT]:
        speedc = speed*2
    else:
        speedc = speed
    dx, dy = get_movement_vector() 
    x += dx * speedc
    if __name__ == "__main__":
        character.x = x
    y += dy * speedc
    if __name__ == "__main__":
        character.y = y
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

def npcmovement(npc, steps, npcspeed):
    #Richtungsvektor vom NPC zum Spieler berechnen
    dx = character.x - npc.x    # Unterschied in x-Richtung
    dy = character.y - npc.y    # Unterschied in y-Richtung

    #Distanz berechnen (Pythagoras)
    dist = (dx**2 + dy**2)**0.5

    #Wenn Distanz != 0: normieren und bewegen
    if dist != 0:               # Wenn noch nicht kolliert, dann weiterverfolgen
        dx /= dist              # Normalisiere x-Komponente (Länge 1)
        dy /= dist              # Normalisiere y-Komponente (Länge 1)

        # 4) NPC in Richtung Spieler bewegen
        npc.x += dx * npcspeed
        npc.y += dy * npcspeed

    #Rückgabe: damit main weiterhin steps = npcmovement vo oben verwenden kann
    return steps

def drawing(screen, character, npc, pixles):
     #check for drawing a pixel
    keys = pygame.key.get_pressed()
    if keys[pygame.K_j]:
        pixles.append(draw(character.x, character.y))
    #Drawing everything
    ostblock.walldraw(screen) #Draw wall
    pygame.draw.rect(screen, (0, 0, 255), character) # Draw player
    pygame.draw.rect(screen, (255, 0, 0), npc) #Draw npc
    for p in pixles:
        pygame.draw.rect(screen, (0, 255, 0), (p)) #Draw pixles


def draw(x,y):
    pixle = pygame.Rect(x, y, 50, 50)
    mapinteraction.add_to_almosteverything(pixle, mapinteraction.almosteverything)
    return pixle

if __name__ == "__main__":

    screen = pygame.display.set_mode((1920, 1080))

    running = True
    while running:
        #Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Added a proper quit check
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        x, y, dx, dy = movement(x, y, speed)
        steps = npcmovement(npc, steps, npcspeed)
        screen.fill((0, 0, 0)) # Clear screen
        drawing(screen, character, npc, pixles)
        pygame.display.update() # Update the display
        clock.tick(60)

    pygame.quit() # Quit pygame properly