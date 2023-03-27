#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define PORT 8888

int main(int argc, char const *argv[]) {
    int sockfd, connfd;
    char buffer[1024];
    struct sockaddr_in servaddr, cliaddr;

    // Créer une socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        printf("Erreur lors de la création de la socket\n");
        exit(0);
    }

    memset(&servaddr, 0, sizeof(servaddr));
    memset(&cliaddr, 0, sizeof(cliaddr));

    // Configuration de l'adresse IP et du port du serveur
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(PORT);

    // Bind la socket avec l'adresse IP et le port du serveur
    if ((bind(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr))) != 0) {
        printf("Erreur lors du bind de la socket\n");
        exit(0);
    }

    // Ecoute les connexions entrantes
    if ((listen(sockfd, 5)) != 0) {
        printf("Erreur lors de l'écoute de la socket\n");
        exit(0);
    }

    int len = sizeof(cliaddr);

    // Accepte la connexion entrante
    connfd = accept(sockfd, (struct sockaddr *)&cliaddr, &len);
    if (connfd < 0) {
        printf("Erreur lors de l'acceptation de la connexion\n");
        exit(0);
    }

    // Ouvre le fichier à envoyer ou recevoir
    FILE *fp;
    if (argc == 2) {
        fp = fopen(argv[1], "rb");
        if (fp == NULL) {
            printf("Erreur lors de l'ouverture du fichier à envoyer\n");
            exit(0);
        }
    } else {
        fp = fopen("received_file", "wb");
        if (fp == NULL) {
            printf("Erreur lors de l'ouverture du fichier à recevoir\n");
            exit(0);
        }
    }

    // Lit ou envoie le contenu du fichier
    while (1) {
        unsigned char buff[1024] = {0};
        int nread = fread(buff, 1, 1024, fp);
        if (nread > 0) {
            if (argc == 2) {
                send(connfd, buff, nread, 0);
            } else {
                recv(connfd, buff, nread, 0);
                fwrite(buff, 1, nread, fp);
            }
        }
        if (nread < 1024) {
            if (feof(fp)) {
                printf("Fin de la lecture/écriture du fichier\n");
            }
            if (ferror(fp)) {
                printf("Erreur lors de la lecture/écriture du fichier\n");
            }
            break;
        }
    }

    // Ferme la socket et le fichier
    close(sockfd);
    close(connfd);
    fclose(fp);
    return 0;
}
