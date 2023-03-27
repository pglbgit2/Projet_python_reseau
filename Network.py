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
###########################################################################################################################



class Network:

    def map_to_file(self, matrice, SIZE_X, SIZE_Y):
        if os.path.exists(path_to_temp_file + "temp.txt"):
            os.remove(path_to_temp_file + "temp.txt")

        f = open("temp.txt", "w")
        visited = []
        text = ""
        for x in range(0,SIZE_X):
            for y in range(0,SIZE_Y):
                if matrice[y][x] not in visited:
                    visited.append(matrice[y][x])
                    phrase = str(matrice[y][x].name) + ';' + str(matrice[y][x].ret_coord())
                    phrase += "\n"
                    text += phrase
        text += 'end;'
        f.write(text)
        f.close()
    
    def get_coord_tuple(self,string): # '(x,y)' to (x,y)
        temp = string.replace('(', '', 1)
        temp = temp.replace(')', '', 1)
        t = temp.split(',')
        return (int(t[0]),int(t[1]))

    def file_to_map(self, matrice, SIZE_X, SIZE_Y):
        if os.path.exists(path_to_temp_file + "\\temp.txt"):
            print("No file 'temp.txt' found.")
            return 0
        f = open("temp.txt", "r")
        text = f.read()
        f.close()
        Bat_list = text.split('\n')
        for k in range(len(Bat_list)):
            arg_parse = Bat_list[k].split(';')
            if arg_parse[0] == 'end':
                break
            (x,y) = self.get_coord_tuple(arg_parse[1])
            idbat = m.name_id[arg_parse[0]]
            m.add_bat(x,y,idbat)

    def delta_to_file(self,delta):
        if delta == '': return 0
        if os.path.exists(path_to_temp_file + "\\mydelta.txt"):
            os.remove(path_to_temp_file + "\\mydelta.txt")
        if os.path.exists(path_to_temp_file + "/mydelta.txt"):
            os.remove(path_to_temp_file + "/mydelta.txt")
        f = open("mydelta.txt", "w")
        f.write(delta)
        delta = ''
        f.close()


    #to test: create file otherDelta.txt with text: l.destroy_grid_delta(19,21,3,5); 
    def file_to_modif(self):
        if not os.path.exists(path_to_temp_file + "\\otherDelta.txt") and not os.path.exists(path_to_temp_file + "/otherDelta.txt"):
            return 0
        f = open("otherDelta.txt", "r")
        text = f.read()
        f.close()
        instruction_list = text.split(';')
        for k in range(len(instruction_list)):
            exec(instruction_list[k])
        try:
            os.remove(path_to_temp_file + "\\otherDelta.txt")
        except: os.remove(path_to_temp_file + "/otherDelta.txt")


    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    #
    csocket_file='./csocket'
    ssocket_file='./sscocket'
    try:
        os.remove(csocket_file)
    except OSError:
        pass
    sock.bind(csocket_file)

    sock.connect(ssocket_file)

    def sendToSender(self):

        try:
            with open('./temp.txt', 'r') as toSend:
                data = toSend.read()
                self.sock.send(data, self.ssocket_file)
        finally:
            pass

    def receiveFromServer(self):
        while True:
            try:
                (bytes, address) = self.sock.recv(1024)
                print("reçu "+ bytes)
                #traitement des modifications
            except socket.error as e:
                print(e)
            