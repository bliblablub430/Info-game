import pygame

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Frau_Weidman_Hunter69")
clock = pygame.time.Clock()

# Player variables
x, y = 700, 500
h, l = 50, 50
speed = 15

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

running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Added a proper quit check
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # --- Game Logic ---
    # 1. Get the normalized direction vector from the function
    dx, dy = get_movement_vector() 
    
    # 2. Update player position in the main loop
    x += dx * speed
    y += dy * speed

    # --- Drawing (all in the main loop) ---
    screen.fill((0, 0, 0)) # Clear screen
    pygame.draw.rect(screen, (0, 0, 255), (x, y, h, l)) # Draw player
    pygame.display.update() # Update the display

    # --- Frame Rate ---
    clock.tick(60)

pygame.quit() # Quit pygame properly