import pygame as pg
import random

pg.init()
pg.font.init()
pic = pg.Surface((200,200))

width, height = 900,900
choice = 1

textboxy = pg.image.load('textbox.png')

while True:

    screen = pg.display.set_mode((900,900))

    dest = 0,0
    dest2 = 450,450


    keys = pg.key.get_pressed()

    if keys[pg.K_a]:
        choice = 2
    elif keys[pg.K_s]:
        choice = 3
    elif keys[pg.K_d]:
        choice = 4
        rand = random.randrange(1, 3)


    # (font-None uses the default font, size, bold, italics, background-stuff that im not really sure about)
    hello = pg.font.SysFont(None, 45, False, False, None)

    if choice == 1:
        text = hello.render("Attack", 1, (255, 153, 18), None)
        text2 = hello.render("Talk", 1, (255, 153, 18), None)
        text3 = hello.render("Run", 1, (255, 153, 18), None)

        dest = 0, 600
        screen.blit(textboxy, dest, area=None, special_flags=0)
        dest = 30, 630
        screen.blit(text, dest)

        dest = 30, 670
        screen.blit(text2, dest)

        dest = 30, 710
        screen.blit(text3, dest)

    elif choice == 2:
        attChoice = 0

        text = hello.render("Punch", 1, (255, 153, 18), None)
        text2 = hello.render("Kick", 1, (255, 153, 18), None)
        text3 = hello.render("Headbutt", 1, (255, 153, 18), None)
        screen.blit(text, (width - 310, 650))


        dest = 0, 600
        screen.blit(textboxy, dest, area=None, special_flags=0)
        dest = 30, 630
        screen.blit(text, dest)

        dest = 30, 670
        screen.blit(text2, dest)

        dest = 30, 710
        screen.blit(text3, dest)

        keysAtt = pg.key.get_pressed()

        if keysAtt[pg.K_q]:
            attChoice = 1
        elif keysAtt[pg.K_w]:
            attChoice = 2
        elif keysAtt[pg.K_e]:
            attChoice = 3

        if attChoice == 1:
            print("You done punched me!")
        elif attChoice == 2:
            print("You done kicked me!")
        elif attChoice == 3:
            print("You done headbutted me!.....weirdo")


    elif choice == 3:
        attChoice = 0

        text = hello.render("Insult", 1, (255, 153, 18), None)
        text2 = hello.render("Compliment", 1, (255, 153, 18), None)
        text3 = hello.render("Meh meh meh", 1, (255, 153, 18), None)
        screen.blit(text, (width - 310, 650))

        dest = 0, 600
        screen.blit(textboxy, dest, area=None, special_flags=0)
        dest = 30, 630
        screen.blit(text, dest)

        dest = 30, 670
        screen.blit(text2, dest)

        dest = 30, 710
        screen.blit(text3, dest)

        keysTalk = pg.key.get_pressed()

        if keysTalk[pg.K_q]:
            attChoice = 1
        elif keysTalk[pg.K_w]:
            attChoice = 2
        elif keysTalk[pg.K_e]:
            attChoice = 3

        if attChoice == 1:
            print("You done insulted me!")
        elif attChoice == 2:
            print("You done complimented me!")
        elif attChoice == 3:
            print("You done creeped me out!.....weirdo")

    elif choice == 4:
        if rand == 1:
            text = hello.render("You are a pansy and tried to run away....you failed", 1, (255, 153, 18), None)
        else:
            text = hello.render("with human feces lubricating your pants,", 1, (255, 153, 18), None)
            textLine2 = hello.render("you manage to run fast enough to escape", 1, (255, 153, 18), None)

        dest = 0, 600
        screen.blit(textboxy, dest, area=None, special_flags=0)
        dest = 30, 630
        screen.blit(text, dest)
        dest = 30, 660
        if rand != 1:
            screen.blit(textLine2, dest)


    pg.display.flip()

