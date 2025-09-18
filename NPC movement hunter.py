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