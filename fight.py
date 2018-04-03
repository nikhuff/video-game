import pygame as pg
import random


pg.init()
pg.font.init()
pic = pg.Surface((200,200))

width, height = 900,900
choice = 1

while True:

    screen = pg.display.set_mode((900,900))

    dest = 0,0
    dest2 = 450,450
    rect1 = pg.Surface((115, 40))
    rect2 = pg.Surface((10, 10))
    rect2.fill((29, 134, 206))


    keys = pg.key.get_pressed()

    if keys[pg.K_a]:
        choice = 2
    elif keys[pg.K_s]:
        choice = 3
    elif keys[pg.K_d]:
        choice = 4
        rand = random.randrange(1, 3)


    if pg.mouse.get_pressed()[0] == True:
        x,y = pg.mouse.get_pos()
        if x > 195 and x < 310 and y > 645 and y < 685:
            choice = 2
        elif x > 395 and x < 510 and y > 645 and y < 685:
            choice = 3
        elif x > 600 and x < 715 and y > 645 and y < 685:
            choice = 4


    # (font-None uses the default font, size, bold, italics, background-stuff that im not really sure about)
    hello = pg.font.SysFont(None, 45, False, False, None)

    if choice == 1:
        text = hello.render("Attack", 1, (255, 153, 18), None)
        text2 = hello.render("Talk", 1, (255, 153, 18), None)
        text3 = hello.render("Run", 1, (255, 153, 18), None)

        rect1 = pg.Surface((1100, 400))
        rect1.fill((29, 134, 206))
        pg.Surface.set_alpha(rect1, 250)

        dest = 0, 600
        screen.blit(rect1, dest, area=None, special_flags=0)
        screen.blit(text, dest)

        dest = 0, 640
        screen.blit(text2, dest)

        dest = 0, 680
        screen.blit(text3, dest)

    elif choice == 2:
        attChoice = 0

        text = hello.render("Punch", 1, (255, 153, 18), None)
        text2 = hello.render("Kick", 1, (255, 153, 18), None)
        text3 = hello.render("Headbutt", 1, (255, 153, 18), None)
        screen.blit(text, (width - 310, 650))

        rect1 = pg.Surface((1100, 400))
        rect1.fill((29, 134, 206))
        pg.Surface.set_alpha(rect1, 250)

        dest = 0, 600
        screen.blit(rect1, dest, area=None, special_flags=0)
        screen.blit(text, dest)

        dest = 0, 640
        screen.blit(rect1, dest, area=None, special_flags=0)
        screen.blit(text2, dest)

        dest = 0, 680
        screen.blit(rect1, dest, area=None, special_flags=0)
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

        rect1 = pg.Surface((1100, 300))
        rect1.fill((29, 134, 206))
        pg.Surface.set_alpha(rect1, 250)

        dest = 0, 600
        screen.blit(rect1, dest, area=None, special_flags=0)
        screen.blit(text, dest)

        dest = 0, 640
        screen.blit(rect1, dest, area=None, special_flags=0)
        screen.blit(text2, dest)

        dest = 0, 680
        screen.blit(rect1, dest, area=None, special_flags=0)
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
            text = hello.render("with human feces lubricating your pants, you manage to run fast enough to escape", 1, (255, 153, 18), None)

        rect1 = pg.Surface((1100, 300))
        rect1.fill((29, 134, 206))
        pg.Surface.set_alpha(rect1, 250)

        dest = 0, 600
        screen.blit(rect1, dest, area=None, special_flags=0)
        screen.blit(text, dest)


    pg.display.flip()

