""" Nouveau Joueur -> Envoie de toutes les données du monde et des joueurs
                        La carte est figé pour les autres joueurs tant que le joueur n'a pas
                        envoyé un 'Done!' aux autres (chronométré).

    En cours de partie -> Chaque joueur effectue une/des commande/s qui seront envoyé dans un buffer
                            pour chaque joueur.
                            Ainsi chaque joueur a sa propre simulation. à la fin du 'TOUR' (adpaté à la vitesse du pire joueur (best effort)
                            500ms Acceptable Max), Tout les joueurs reçoivent un 'Done!' et le tour suivant débute.

                            """
import functools
import os
import Model.matrice as m
import socket
import errno
import struct
import time
import select
import sys
from View.settings import path_to_temp_file
from Model import logique as l
import copy as cp
import subprocess
import threading
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

#fonction c / python : recevoir envoyer
# astuce: fichier commence par #machin et se termine par end 

class Network:

    def __init__(self) -> None:
        if len(sys.argv) == 1:
            threadprogc = threading.Thread( target = subprocess.call, args = ['./transm'])
        if len(sys.argv) == 3:
            print(sys.argv[1])
            print(sys.argv[2])
            threadprogc = threading.Thread( target = subprocess.call, args = [['./transm', sys.argv[1], sys.argv[2]]])
        if len(sys.argv) == 4:
            threadprogc = threading.Thread( target = subprocess.call, args = [['./transm', sys.argv[1], sys.argv[2], sys.argv[3]]])
        
        
        threadprogc.start()
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.ssocket_file=path_to_temp_file+'/ssocket'
        print('avant')
        test = 0
        while test == 0:
            try:
                self.sock.connect(self.ssocket_file)
                test = 1
            except:
                continue
        print('apres')
        self.rdescriptors = []
        self.wdescriptors = []
        self.xdescriptors = []

    def map_to_file(self, matrice_bat, matrice_walk, SIZE_X, SIZE_Y):
        if os.path.exists(path_to_temp_file + "/temp.txt"):
            os.remove(path_to_temp_file + "/temp.txt")
        if os.path.exists(path_to_temp_file + "\\temp.txt"):
            os.remove(path_to_temp_file + "\\temp.txt")
        f = open("temp.txt", "w")
        f.write('#welcome\n')
        visited = []
        text = ""
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                if matrice_bat[y][x] not in visited:
                    obj = matrice_bat[y][x]
                    visited.append(obj)
                    phrase = str(obj.name) + ';' + str(obj.ret_coord()) + ';' + obj.texture

                    if issubclass(type(obj), l.m.pa.b.Batiment):
                        phrase += ';' + str(obj.curEmployees)
                        phrase += ';' + str(obj.hasRecruteur)

                        if issubclass(type(obj), l.m.mais.Maison):
                            phrase += ';'
                            phrase += str(obj.curpop) + ';' + str(obj.employed) + ';'
                            phrase += str(obj.nourriture[0][1])

                        elif issubclass(type(obj), l.m.war.Warehouse) or issubclass(type(obj),
                                                                                    l.m.g.Granary) or issubclass(
                            type(obj), l.m.mar.Market):
                            phrase += ';'
                            phrase += str(obj.nourriture[0][1])

                        elif isinstance(obj, l.m.f.Ferme):
                            phrase += ';'
                            phrase += str(obj.ind_Harv)
                    phrase += "\n"
                    text += phrase
        text += "---;\n"
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                if issubclass(type(matrice_bat[y][x]), l.m.pa.Path):
                    walkers = matrice_walk[y][x]
                    if walkers[0].name != "no Walker":
                        for k in range(len(walkers)):
                            if walkers[k].dest_x == -1 or walkers[k].tab_path != []:
                                phrase = ""
                                phrase += str(walkers[k].name) + ';(' + str(walkers[k].x) + ',' + str(
                                    walkers[k].y) + ');' \
                                          + str(walkers[k].ttl) + ';' + self.get_string_tab_path(
                                    walkers[k].tab_path) + ';' + str(walkers[k].batiment.ret_coord()) \
                                          + ';(' + str(walkers[k].dest_x) + ',' + str(walkers[k].dest_y) + ');(' + str(
                                    walkers[k].prev_x) \
                                          + ',' + str(walkers[k].prev_y) + ')'
                                if walkers[k].name == "Food_guy":
                                    phrase += ';' + str(walkers[k].role) + ';'
                                    phrase += str(walkers[k].cargaison_nourriture[0][1])
                                if walkers[k].name == "Delivery_Guy":
                                    phrase += ';' + str(walkers[k].cargaison_nourriture[0][1])
                                if hasattr(walkers[k], "bat_destination") is not False and walkers[
                                    k].bat_destination is not None:
                                    phrase += ';' + str(walkers[k].bat_destination.ret_coord())
                                else:
                                    phrase += ';None'
                                phrase += "\n"
                                text += phrase
        text += '---;\n'
        text += str(m.get_Population()) + ';' + str(m.unemployed) + ';' + str(m.Nb_immigrant) + ';\n'
        text += str(m.Mat_route) + ';\n'
        text += str(m.Mat_fire) + ';\n'
        text += str(m.Mat_water) + ';\n'
        text += 'end;'
        f.write(text)
        f.close()

    def get_string_tab_path(self, tab_path):

        print("called")
        txt = ''
        if len(tab_path) == 0:
            return ''
        print(tab_path)
        for x in tab_path:
            print(x)
            (a, b) = x
            txt += '(' + str(a) + ',' + str(b) + ')' + '|'
        if len(txt) != 0:
            txt = txt[:-1]
        print('txt:', txt)
        return txt

    def get_tab_path_string(self, string):
        if string == '':
            return []
        tab = []
        coord_list = string.split('|')
        for x in coord_list:
            tab.append(self.get_coord_tuple(x))
        return tab

    def get_coord_tuple(self, string):  # '(x,y)' to (x,y)
        temp = string.replace('(', '', 1)
        temp = temp.replace(')', '', 1)
        t = temp.split(',')
        return int(t[0]), int(t[1])

    def file_to_map(self, matrice, SIZE_X, SIZE_Y):
        if not os.path.exists(path_to_temp_file + "\\temp.txt") and not os.path.exists(path_to_temp_file + "/temp.txt"):
            print("No file 'temp.txt' found.")
            return 0
        f = open("temp.txt", "r")
        text = f.read()
        f.close()
        list = text.split('\n')
        k = 1
        while True:
            arg_parse = list[k].split(';')
            if arg_parse[0] == '---':
                break
            (x, y) = self.get_coord_tuple(arg_parse[1])
            idbat = m.name_id[arg_parse[0]]
            m.add_bat(x, y, idbat)
            bat = matrice[y][x]
            bat.texture = arg_parse[2]
            if issubclass(type(bat), l.m.pa.b.Batiment):
                bat.curEmployees = int(arg_parse[3])
                bat.hasRecruteur = int(arg_parse[4])
                if issubclass(type(bat), l.m.mais.Maison):
                    bat.curpop = int(arg_parse[5])
                    bat.employed = int(arg_parse[6])
                    bat.nourriture[0][1] = int(arg_parse[7])
                elif issubclass(type(bat), l.m.war.Warehouse) or issubclass(type(bat), l.m.g.Granary) or issubclass(
                        type(bat), l.m.mar.Market):
                    bat.nourriture[0][1] = int(arg_parse[5])
                elif issubclass(type(bat), l.m.f.Ferme):
                    bat.ind_Harv = int(arg_parse[5])
                else:
                    pass
            else:
                pass
            k += 1
        k += 1
        while True:
            arg_parse = list[k].split(';')
            if arg_parse[0] == '---':
                break
            walker_name = arg_parse[0]
            (x, y) = self.get_coord_tuple(arg_parse[1])
            (bx, by) = self.get_coord_tuple(arg_parse[4])
            t = arg_parse[len(arg_parse) - 1]
            if t != 'None':
                (bdx, bdy) = self.get_coord_tuple(t)
                (dx, dy) = self.get_coord_tuple(arg_parse[5])
                (px, py) = self.get_coord_tuple(arg_parse[6])
                print(walker_name)
                perso = m.add_perso(x, y, walker_name, m.Mat_perso, matrice[by][bx], matrice[bdy][bdx])
                perso.dest_x = dx
                perso.dest_y = dy
                perso.prev_x = px
                perso.prev_y = py
                if perso.name == "Food_guy":
                    perso.cargaison_nourriture[0][1] = int(arg_parse[len(arg_parse) - 2])
                    perso.role = arg_parse[len(arg_parse) - 3]
                    perso.tab_path = self.get_tab_path_string(arg_parse[3])
                elif perso.name == "Delivery_Guy":
                    perso.cargaison_nourriture[0][1] = int(arg_parse[len(arg_parse) - 2])
                    perso.tab_path = self.get_tab_path_string(arg_parse[3])
            else:
                if walker_name == "Immigrant":
                    perso = m.add_perso(x, y, walker_name, m.Mat_perso, matrice[by][bx], matrice[by][bx])
                    perso.tab_path = self.get_tab_path_string(arg_parse[3])
                else:
                    perso = m.add_perso(x, y, walker_name, m.Mat_perso, matrice[by][bx], None)
            k += 1

        k += 1

        arg_parse = list[k].split(';')
        l.m.Population = int(arg_parse[0])
        l.m.unemployed = int(arg_parse[1])
        l.m.Nb_immigrant = int(arg_parse[2])

        k += 1
        arg_parse = list[k].split(';')
        l.m.Mat_route = eval(arg_parse[0])

        k += 1
        arg_parse = list[k].split(';')
        l.m.Mat_fire = eval(arg_parse[0])

        k += 1
        arg_parse = list[k].split(';')
        l.m.Mat_water = eval(arg_parse[0])

    def delta_to_file(self, delta):
        if delta == '': return 0
        if os.path.exists(path_to_temp_file + "\\mydelta.txt"):
            os.remove(path_to_temp_file + "\\mydelta.txt")
        if os.path.exists(path_to_temp_file + "/mydelta.txt"):
            os.remove(path_to_temp_file + "/mydelta.txt")
        f = open("mydelta.txt", "w")
        f.write("#delta;")
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
        for k in range(1,len(instruction_list)):
            exec(instruction_list[k])
        try:
            os.remove(path_to_temp_file + "\\otherDelta.txt")
        except:
            os.remove(path_to_temp_file + "/otherDelta.txt")



    def sendToServer(self, file_name): #not actually a server

        try:
            with open('./'+ file_name, 'r') as toSend:
                data = toSend.read()
                arr = bytes(data, 'utf-8')
                arr2 = struct.pack(">H", 8)
                # print(arr2)
                time.sleep(1)
                self.sock.send(arr)
        finally:
            pass

    def receiveFromServer(self):
        while True:
            try:
                bytes = self.sock.recv(1024)
                print("reçu ")
                buf = bytes.decode('utf-8')
                # traitement des modifications
                return buf
            except socket.error as e:
                print(e)
                return -1


    def GestionEntreesSortie(self):
        if self.rdescriptors == []:
            self.rdescriptors.append(self.sock)

        rlist, wlist, xlist = select.select(self.rdescriptors, self.wdescriptors, self.xdescriptors)

        if rlist != []:
            assert rlist[0] == self.sock
            buf = self.receiveFromServer()
            if buf == -1:
                assert False
            else:
                if buf[0] == '#':

                    fline = buf.split('\n')
                    print("fline = ",fline)
                    if fline[0] == '#newco': #cas demande d'envoie de données complete
                        
                        self.map_to_file(l.m.Mat_batiment, l.m.Mat_perso, m.nb_cases_x, m.nb_cases_y)
                        self.sendToServer('temp.txt')
                        print('send newco')

                    if fline[0] == '#delta': # cas envoi de delta
                        if self.delta_to_file(l.m.delta) == 0:
                            pass
                        else:
                            self.sendToServer("delta.txt")
                            # envoi du fichier delta

                    if fline[0] == '#welcome': # cas reception ensemble donne jeu
                        self.file_to_map(l.m.Mat_batiment, m.nb_cases_x, m.nb_cases_y)
                        print('receiv welcome')


                else:
                    print(buf)
                    print('ERROR: buffer seems to be corrupted')
                    print('quitting now...')
                    assert False
                assert False


Net = Network()
while True:
    Net.GestionEntreesSortie()