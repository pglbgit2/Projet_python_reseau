import pygame as pg
import socket

from Interface.Data_controller import *
from Interface.InputBoxName import *
from View.game import *
from Model.logique import *


def main():
    # Global varibles

    # Variable pour les boucles dans le jeu
    running = True
    global Cur_page
    Cur_page = None
    playing = True
    Launch = True

    pg.init()
    pg.mixer.init()
    global screen
    screen = pg.display.set_mode((0, 0))
    clock = pg.time.Clock()
    pg.mixer.init()
    pg.mixer.music.load("Rome4.mp3")
    pg.mixer.music.play()
    set_screen_tittle(screen)

    Game_terminus = Game(screen, clock)

    # implement game

    # Game = game.Game(screen, clock)

    while running:

        clock.tick(60)
        mouse_track = pg.mouse.get_pos()
        pg.display.update()
        pg.display.flip()

        while Launch:  # Launch

            pg.display.flip()
            mouse_track = pg.mouse.get_pos()

            for event in pg.event.get():

                if event.type == pg.QUIT:
                    running = False
                    Launch = False
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEMOTION:

                    if Cur_page == "Home":
                        HP_exit.transparenci(mouse_track, screen)
                        HP_load_game.transparenci(mouse_track, screen)
                        HP_newc.transparenci(mouse_track, screen)
                        HP_join_game.transparenci(mouse_track, screen)
                        pg.display.flip()

                    if Cur_page == "Join":
                        JP_connect.transparenci(mouse_track, screen)

                if event.type == pg.KEYDOWN and event.unicode:

                    if Cur_page == "Select":
                        SP_input.ajout_char(event, screen)

                if event.type == pg.MOUSEBUTTONDOWN:

                    if Cur_page == "Home":  # Si on se trouve sur la page Home

                        if HP_exit.overhead(mouse_track, screen):
                            running = False
                            Launch = False
                            pg.quit()
                            sys.exit()

                        elif HP_newc.overhead(mouse_track, screen):
                            Cur_page = "Select"
                            set_screen_SP(screen)
                            SP_input.draw(screen)

                        elif HP_load_game.overhead(mouse_track, screen):
                            Cur_page = "Restaure"
                            RP_page.draw(screen)
                            disable_all()

                        elif HP_join_game.overhead(mouse_track, screen):
                            Cur_page = "Join"
                            set_screen_join_page(screen)
                            disable_all()

                    elif Cur_page == "Join":

                        if JP_connect.overhead(mouse_track, screen):
                            print("Enter IP address here (leave empty if new game):")
                            IP = input()
                            if IP == "":
                                print("New game created ! IP address is : ", end="")
                                print(socket.gethostbyname(socket.gethostname()))
                            else:
                                print("Attempting connection to ", end="")
                                print(IP, end="")
                                print(" ...")
                            pg.mixer.music.load("Rome1.mp3")
                            pg.mixer.music.play()
                            Launch = False
                            playing = True
                            disable_all_JP_button()

                    elif Cur_page == "Select":  # Si ony se trouve sur la page Select

                        # Erreur dans la conception avec les rectangle 

                        if SP_go_home_txt_R.collidepoint(mouse_track):
                            Cur_page = "Home"
                            set_screen_HP(screen)

                        if SP_validate_txt_R.collidepoint(mouse_track):
                            pg.mixer.music.load("Rome1.mp3")
                            pg.mixer.music.play()
                            Launch = False
                            playing = True

                        SP_input.collide(mouse_track)

                    elif Cur_page == "Restaure":

                        action = RP_page.action()

                        if action == go_to_home_page:
                            Cur_page = "Home"
                            set_screen_HP(screen)

                        elif action == Play_sg_1 and RP_page.save_1.text not in Emplacements:
                            pg.mixer.music.load("Rome1.mp3")
                            pg.mixer.music.play()
                            Launch = False
                            playing = True
                            SP_input.text = RP_page.save_1.text
                            l.event_to_logic(l.Nume_load, None, None, RP_page.save_1.text)
                        elif action == Play_sg_2 and RP_page.save_2.text not in Emplacements:
                            pg.mixer.music.load("Rome1.mp3")
                            pg.mixer.music.play()
                            Launch = False
                            playing = True
                            SP_input.text = RP_page.save_2.text
                            l.event_to_logic(l.Nume_load, None, None, RP_page.save_2.text)
                        elif action == Play_sg_3 and RP_page.save_3.text not in Emplacements:
                            pg.mixer.music.load("Rome1.mp3")
                            pg.mixer.music.play()
                            Launch = False
                            playing = True
                            SP_input.text = RP_page.save_3.text
                            l.event_to_logic(l.Nume_load, None, None, RP_page.save_3.text)

                    else:  # Si on se trouve dans l'écran titre

                        Cur_page = "Home"
                        set_screen_HP(screen)

                elif event.type == pg.VIDEORESIZE:
                    pg.display.update()
                elif event.type == pg.VIDEOEXPOSE:
                    pg.display.update()

        while playing:
            playing = Game_terminus.run()

            if not playing:
                Cur_page = "Home"
                set_screen_HP(screen)
                Launch = True


if __name__ == "__main__":
    main()
