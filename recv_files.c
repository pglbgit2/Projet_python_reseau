#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define PORT 8899

int main(int argc, char const *argv[]) {
    int sockfd;
    char buffer[1024];
    struct sockaddr_in servaddr;

    // Vérifie que le nombre d'arguments est correct
    if (argc != 3) {
        printf("Usage: %s <adresse IP du serveur> <nom du fichier>\n", argv[0]);
        exit(0);
    }

    // Créer une socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        printf("Erreur lors de la création de la socket\n");
        exit(0);
    }

    memset(&servaddr, 0, sizeof(servaddr));

    // Configuration de l'adresse IP et du port du serveur
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr(argv[1]);
    servaddr.sin_port = htons(PORT);

    // Connecte la socket au serveur distant
    if (connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) != 0) {
        printf("Erreur lors de la connexion au serveur\n");
        exit(0);
    }

    // Ouvre le fichier à recevoir
    FILE *fp = fopen(argv[2], "wb");
    if (fp == NULL) {
        printf("Erreur lors de l'ouverture du fichier\n");
        exit(0);
    }

    // Lit les données envoyées par le serveur et les écrit dans le fichier
    while (1) {
        unsigned char buff[1024] = {0};
        int nread = read(sockfd, buff, 1024);
        if (nread > 0) {
            fwrite(buff, 1, nread, fp);
        }
        if (nread < 1024) {
            if (feof(fp)) {
                printf("Fin de la réception du fichier\n");
            }
            if (ferror(fp)) {
                printf("Erreur lors de la réception du fichier\n");
            }
            break;
        }
    }

    // Ferme la socket et le fichier
    close(sockfd);
    fclose(fp);

    return 0;
}
