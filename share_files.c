#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define PORT 8888


int send_file(const char* file_name, int sockfd){
    struct sockaddr_in servaddr;
    struct sockaddr_in cliaddr;
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
    int connfd = accept(sockfd, (struct sockaddr *)&cliaddr, &len);
    if (connfd < 0) {
        printf("Erreur lors de l'acceptation de la connexion\n");
        exit(0);
    }

    // Ouvre le fichier à envoyer
    FILE *fp = fopen(file_name, "rb");
    if (fp == NULL) {
        printf("Erreur lors de l'ouverture du fichier\n");
        exit(0);
    }

    // Lit le contenu du fichier et l'envoie au client
    while (1) {
        unsigned char buff[1024] = {0};
        int nread = fread(buff, 1, 1024, fp);
        if (nread > 0) {
            write(connfd, buff, nread);
        }
        if (nread < 1024) {
            if (feof(fp)) {
                printf("Fin de la lecture du fichier\n");
            }
            if (ferror(fp)) {
                printf("Erreur lors de la lecture du fichier\n");
            }
            break;
        }
    }

    // Ferme la socket et le fichier
    close(sockfd);
    fclose(fp);
    return 0;
}

int receive_file(const char* ip_adresse, const char* file_name, int sockfd){
    struct sockaddr_in servaddr;
    memset(&servaddr, 0, sizeof(servaddr));

    // Configuration de l'adresse IP et du port du serveur
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr(ip_adresse);
    servaddr.sin_port = htons(PORT);

     // Connecte la socket au serveur distant
    if (connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) != 0) {
        printf("Erreur lors de la connexion au serveur\n");
        exit(0);
    }

    // Ouvre le fichier à recevoir
    FILE *fp = fopen(file_name, "wb");
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
int main(int argc, char const *argv[]) {
    int sockfd;
    char buffer[1024];

    // Créer une socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        printf("Erreur lors de la création de la socket\n");
        exit(0);
    }

    if (argc == 3){
        receive_file(argv[1], argv[2],sockfd);
    }else if(argc==2){
        send_file(argv[1], sockfd);
    }else{
        printf("erreur au nombre d'arguments");
        exit(0);
    }
}
