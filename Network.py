""" Nouveau Joueur -> Envoie de toutes les données du monde et des joueurs
                        La carte est figé pour les autres joueurs tant que le joueur n'a pas
                        envoyé un 'Done!' aux autres (chronométré).

    En cours de partie -> Chaque joueur effectue une/des commande/s qui seront envoyé dans un buffer
                            pour chaque joueur.
                            Ainsi chaque joueur a sa propre simulation. à la fin du 'TOUR' (adpaté à la vitesse du pire joueur (best effort)
                            500ms Acceptable Max), Tout les joueurs reçoivent un 'Done!' et le tour suivant débute.

                            """
import os
import Model.matrice as m
from View.settings import path_to_temp_file
from Model import logique as l
import copy as cp


################################### LISTE DES OBJECTIFS PARTIE LOGIQUE ####################################################
# map_to_file doit pouvoir transformer l'integralité du jeu: walker + contenu des batiments -> texte                      #
# file_to_map doit pouvoir transformer du texte en elements de jeu: texte -> walker  + contenu des batiments              #
# les batiments sont déjà géré par les deux fonctions, mais pas leur contenu                                              #
# faire une fonction qui va gérer la connexion d'un nouvel utilisateur: envoi de l'ensemble des données du jeu            #
# sachant que les données sont collectées à partir de map_to_file                                                         #
# faire fonction qui gère le cas où on est le nouvel utilisateur: reception et mise a jours des données du jeu            #
# sachant que les donnée peuvent etre extraite a partir de file_to_map                                                    #
# mettre a jours les deltas: gérer effondrement et feu                                                                    #
# Probleme identification walker-batiment: utiliser numerotation ? SOLUTION : SUPPRIMER LE D2PLACEMENT AL2ATOIRE          #
###########################################################################################################################


class Network:

    def map_to_file(self, matrice_bat, matrice_walk, SIZE_X, SIZE_Y):
        if os.path.exists(path_to_temp_file + "temp.txt"):
            os.remove(path_to_temp_file + "temp.txt")

        f = open("temp.txt", "w")
        visited = []
        text = ""
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                if matrice_bat[y][x] not in visited:
                    obj = matrice_bat[y][x]
                    visited.append(obj)
                    phrase = str(obj.name) + ';' + str(obj.ret_coord()) + ';' + obj.texture

                    if issubclass(obj, l.m.pa.b.Batiment):
                        phrase += ';' + str(obj.curEmployees)

                        if issubclass(obj, l.m.mais.Maison):
                            phrase += ';'
                            phrase += str(obj.curpop) + ';' + str(obj.employed) + ';'
                            phrase += str(obj.nourriture[0][1])

                        elif issubclass(obj, l.m.war.Warehouse) or issubclass(obj, l.m.g.Granary) or issubclass(obj,
                                                                                                                l.m.mar.Market):
                            phrase += ';'
                            phrase += str(obj.nourriture[0][1])

                        elif issubclass(obj, l.m.f.Ferme):
                            phrase += ';'
                            phrase += str(obj.ind_Harv)

                            # Les walkers ne peuvent pas être relié a un batiment puisqu'ils n'existent pas encore
                            """ walkers = matrice_walk[y][x]   # Ils seront reliés après dans la décapsulation de temp.txt
                            if walkers[0].name != "no Walker":
                                phrase += ';'
                                for k in len(walkers):
                                    phrase += str(walkers[k].name) + '(' + str(walkers[k].x) + ',' + str(walkers[k].y) + ');'
                                    + str(walkers[k].)
                            """


                    phrase += "\n"
                    text += phrase
        text += "---;\n"
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                if issubclass(matrice_bat[y][x], l.m.pa.Path):
                    walkers = matrice_walk[y][x]
                    if walkers[0].name != "no Walker":
                        for k in len(walkers):
                            phrase = ""
                            phrase += str(walkers[k].name) + ';(' + str(walkers[k].x) + ',' + str(walkers[k].y) + ');'\
                            + str(walkers[k].ttl) + ';' + self.get_string_tab_path(walkers[k].tab_path) + ';' + str(walkers[k].batiment.ret_coord())\
                            + ';(' + str(walkers[k].dest_x) + ',' + str(walkers[k].dest_y) + ');(' + str(walkers[k].prev_x)\
                            + ',' + str(walkers[k].prev_y) + ');(' + str(walkers[k].nx) + ',' + str(walkers[k].ny) + ');'
                            phrase += "\n"
                            text += phrase
        text += 'end;'
        f.write(text)
        f.close()
    def get_string_tab_path(self,tab_path):
        txt = ''
        for x in tab_path :
            (a,b) = x
            txt += '('+str(a)+','+str(b)+')'+'|'
        return txt
    def get_coord_tuple(self, string):  # '(x,y)' to (x,y)
        temp = string.replace('(', '', 1)
        temp = temp.replace(')', '', 1)
        t = temp.split(',')
        return (int(t[0]), int(t[1]))

    def file_to_map(self, matrice, SIZE_X, SIZE_Y):
        if os.path.exists(path_to_temp_file + "\\temp.txt"):
            print("No file 'temp.txt' found.")
            return 0
        f = open("temp.txt", "r")
        text = f.read()
        f.close()
        list = text.split('\n')
        k=0
        while True:
            arg_parse = list[k].split(';')
            if arg_parse[0] == '---':
                break
            (x, y) = self.get_coord_tuple(arg_parse[1])
            idbat = m.name_id[arg_parse[0]]
            m.add_bat(x, y, idbat)
            bat = matrice[y][x]
            bat.texture = arg_parse[2]
            if issubclass(bat, l.m.pa.b.Batiment):
                bat.curEmployees = int(arg_parse[3])
                if issubclass(bat, l.m.mais.Maison):
                    bat.curpop = int(arg_parse[4])
                    bat.employed = int(arg_parse[5])
                    bat.nourriture[0][1] = int(arg_parse[6])
                elif issubclass(bat, l.m.war.Warehouse) or issubclass(bat, l.m.g.Granary) or issubclass(bat, l.m.mar.Market):
                    bat.nourriture[0][1] = int(arg_parse[4])
                elif issubclass(bat, l.m.f.Ferme):
                    bat.ind_Harv = int(arg_parse[4])
                else:
                    pass
            else:
                pass
            k+=1
        k+=1
        while True:
            arg_parse = list[k].split(';')
            if arg_parse[0] == 'end':
                break
            walker_name = arg_parse[0]
            (x, y) = self.get_coord_tuple(arg_parse[1])

            m.add_perso(x, y, walker_name, m.Mat_perso, matrice[y][x], )




    def delta_to_file(self, delta):
        if delta == '': return 0
        if os.path.exists(path_to_temp_file + "\\mydelta.txt"):
            os.remove(path_to_temp_file + "\\mydelta.txt")
        if os.path.exists(path_to_temp_file + "/mydelta.txt"):
            os.remove(path_to_temp_file + "/mydelta.txt")
        f = open("mydelta.txt", "w")
        f.write(delta)
        delta = ''
        f.close()

    # to test: create file otherDelta.txt with text: l.destroy_grid_delta(19,21,3,5);
    def file_to_modif(self):
        if not os.path.exists(path_to_temp_file + "\\otherDelta.txt") and not os.path.exists(
                path_to_temp_file + "/otherDelta.txt"):
            return 0
        f = open("otherDelta.txt", "r")
        text = f.read()
        f.close()
        instruction_list = text.split(';')
        for k in range(len(instruction_list)):
            exec(instruction_list[k])
        try:
            os.remove(path_to_temp_file + "\\otherDelta.txt")
        except:
            os.remove(path_to_temp_file + "/otherDelta.txt")
