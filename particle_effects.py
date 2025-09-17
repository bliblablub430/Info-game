import pygame, random

particles = []  # Hier werden alle Partikel gespeichert

def spawn_particles(x, y):
    # Erzeugt 10 neue Partikel an der Position (x, y)
    for _ in range(10):
        # Jeder Partikel bekommt eine zufällige Geschwindigkeit und Größe
        particles.append([x, y, random.randint(-3,3), random.randint(-3,3), random.randint(4,8)])

def update_particles(surface): # Visualisierung von Partcles 
    # Aktualisiert und zeichnet alle Partikel
    for p in particles[:]:  # Kopie der Liste, damit wir sie ändern können
        p[0] += p[2]        # X-Position ändern (Bewegung)
        p[1] += p[3]        # Y-Position ändern (Bewegung)
        p[4] -= 1           # Größe verkleinern (Partikel "verblasst")
        pygame.draw.circle(surface, (255,255,0), (int(p[0]), int(p[1])), max(1,p[4]))  # Gelber Kreis zeichnen
        if p[4] <= 0:       # Wenn der Partikel zu klein ist, löschen
            particles.remove(p)