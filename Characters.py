import pygame
import ostblock

pygame.init()
pygame.display.set_caption("Frau_Weidman_Hunter69")
clock = pygame.time.Clock()

# Player variables
x, y = 700, 500
h, l = 50, 50
speed = 5
character = pygame.Rect(x, y, h, l)

xn, yn = 800, 600
hn, ln = 50, 50
steps = 0
npcspeed = 5
npc = pygame.Rect(xn, yn, hn, ln)

pixles = []

def movement(x, y, speed):
    dx, dy = get_movement_vector() 
    x += dx * speed
    y += dy * speed
    return x, y, (dx*speed), (dy*speed)

def get_movement_vector():
    dx, dy = 0, 0  # Start with no movement
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_d]:
        dx += 1
    if keys[pygame.K_a]:
        dx -= 1
    if keys[pygame.K_w]:
        dy -= 1
    if keys[pygame.K_s]:
        dy += 1
        

    # Normalize the vector (so diagonal movement isn't faster)
    if dx != 0 or dy != 0:
        vector_len = (dx**2 + dy**2)**0.5
        dx = dx / vector_len
        dy = dy / vector_len
        
    return dx, dy # Return the calculated direction

def npcmovement(npc, steps, npcspeed):
    #NPC algorythm
    if steps < 20:
        npc.x += npcspeed
    elif steps >= 20 and steps < 40:
        npc.y += npcspeed
    elif steps >= 40 and steps < 60:
        npc.x -= npcspeed
    elif steps >= 60 and steps < 80:
        npc.y -= npcspeed
    elif steps == 80:
        steps = 0
    steps += 1
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
    return pygame.Rect(x, y, 50, 50)

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

        x, y = movement(x, y, speed)
        steps = npcmovement(npc, steps, npcspeed)
        screen.fill((0, 0, 0)) # Clear screen
        drawing(screen, character, npc, pixles)
        pygame.display.update() # Update the display
        clock.tick(60)

    pygame.quit() # Quit pygame properly