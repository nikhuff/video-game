import pygame

pygame.mixer.init()

city = pygame.mixer.Sound('./assets/audio/city.wav')
title = pygame.mixer.Sound('./assets/audio/karmaNES.wav')
battle = pygame.mixer.Sound('./assets/audio/HarmonicMinor.wav')
menu_move = pygame.mixer.Sound('./assets/audio/sfx_menu_move1.wav')
menu_select = pygame.mixer.Sound('./assets/audio/sfx_sounds_pause2_in.wav')
game_start = pygame.mixer.Sound('./assets/audio/sfx_sounds_pause2_out.wav')
NPC_Interact = pygame.mixer.Sound('./assets/audio/NPC_Interact3.wav')
prologue = pygame.mixer.Sound('./assets/audio/prologue.wav')
punch = pygame.mixer.Sound('./assets/audio/sfx_wpn_punch4.wav')
