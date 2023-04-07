#include <arpa/inet.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/sendfile.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <unistd.h>

#include "connexion.h"

void *send_file(void *arg) {
  int client_socket = *(int *)arg;
  char filename[1024];

  while (1) {
    printf("Entrez le nom du fichier à envoyer : ");
    fgets(filename, 1024, stdin);
    filename[strcspn(filename, "\n")] = 0;

    int file_fd = open(filename, O_RDONLY);
    if (file_fd < 0) {
      perror("Erreur lors de l'ouverture du fichier");
      continue;
    }

    struct stat file_stat;
    fstat(file_fd, &file_stat);

    send(client_socket, &file_stat.st_size, sizeof(off_t), 0);
    send(client_socket, filename, 1024, 0);
    sendfile(client_socket, file_fd, NULL, file_stat.st_size);

    close(file_fd);
  }

  return NULL;
}

void *receive_file(void *arg) {
  int client_socket = *(int *)arg;
  char filename[1024];

  while (1) {
    off_t filesize;
    recv(client_socket, &filesize, sizeof(off_t), 0);
    recv(client_socket, filename, 1024, 0);

    int file_fd = open(filename, O_WRONLY | O_CREAT, 0644);
    if (file_fd < 0) {
      perror("Erreur lors de la création du fichier");
      continue;
    }

    off_t remaining = filesize;
    ssize_t received;
    char buffer[4096];
    while (remaining > 0 && (received = recv(client_socket, buffer, 4096, 0)) > 0) {
      write(file_fd, buffer, received);
      remaining -= received;
    }

    close(file_fd);
    printf("Fichier '%s' reçu.\n", filename);
  }

  return NULL;
}

int setup_server(int port) {
    int server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket < 0) {
        perror("Erreur lors de la création du socket serveur");
        exit(EXIT_FAILURE);
    }

    struct sockaddr_in server_address;
    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = INADDR_ANY;
    server_address.sin_port = htons(port);

    if (bind(server_socket, (struct sockaddr *)&server_address, sizeof(server_address)) < 0) {
        perror("Erreur lors du bind");
        exit(EXIT_FAILURE);
    }

    if (listen(server_socket, 1) < 0) {
        perror("Erreur lors de l'écoute");
        exit(EXIT_FAILURE);
    }

    printf("Joueur en écoute sur le port %d\n", port);

    struct sockaddr_in client_address;
    socklen_t client_address_len = sizeof(client_address);
    int client_socket = accept(server_socket, (struct sockaddr *)&client_address, &client_address_len);
    if (client_socket < 0) {
    perror("Erreur lors de l'acceptation de la connexion");
    exit(EXIT_FAILURE);
    }

    printf("Client connecté : %s\n", inet_ntoa(client_address.sin_addr));

    close(server_socket);
    return client_socket;
}

int setup_client(const char *address, int port) {
    int client_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (client_socket < 0) {
    perror("Erreur lors de la création du socket client");
    exit(EXIT_FAILURE);
    }

    struct sockaddr_in server_address;
    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(port);

    if (inet_pton(AF_INET, address, &server_address.sin_addr) <= 0) {
    perror("Erreur lors de la conversion de l'adresse");
    exit(EXIT_FAILURE);
    }

    if (connect(client_socket, (struct sockaddr *)&server_address, sizeof(server_address)) < 0) {
    perror("Erreur lors de la connexion");
    exit(EXIT_FAILURE);
    }

    printf("Connecté au joueur : %s\n", address);

    return client_socket;
}