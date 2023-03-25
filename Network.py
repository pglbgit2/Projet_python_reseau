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
from View.settings import path_to_temp_file
from Model import logique as l
import copy as cp

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
            batiment = matrice[y][x]

    def delta_to_file(self,delta):
        if os.path.exists(path_to_temp_file + "temp.txt"):
            os.remove(path_to_temp_file + "temp.txt")
        f = open("temp.txt", "w")
        f.write(delta)
        delta = ''
        f.close()

    def file_to_modif(self):
        if os.path.exists(path_to_temp_file + "\\temp.txt"):
            return 0

        f = open("temp.txt", "r")
        text = f.read()
        f.close()
        instruction_list = text.split(';')
        for k in range(len(instruction_list)):
            exec(instruction_list[k])
        os.remove(path_to_temp_file + "\\temp.txt")


    def sendToSender(self):
        #Création socket
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        #
        socket_file='./socket'
        try:
            os.remove(socket_file)
        except OSError:
            pass
        sock.bind(socket_file)

        sock.listen(1)

        print('Attente connection')
        connection, client_address = sock.accept()

        try:

            with open('./temp.txt', 'r') as toSend:
                data = toSend.read()

            connection.sendall(data.encode())

        finally:
            connection.close()
            sock.close()