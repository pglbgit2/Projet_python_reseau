Compilation: gcc -o exchange main.c connexion.c -lpthread

Premier joueur: ./exchange 0.0.0.0 <port>

Deuxième joueur: ./exchange <IP du premier joueur> <port>