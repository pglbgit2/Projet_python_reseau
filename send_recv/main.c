#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include "connexion.h"
#include <string.h>

int main(int argc, char *argv[]) {
  if (argc != 3) {
    fprintf(stderr, "Utilisation : %s <adresse IP> <port>\n", argv[0]);
    exit(EXIT_FAILURE);
  }

  const char *address = argv[1];
  int port = atoi(argv[2]);
  int client_socket;

  if (strcmp(address, "0.0.0.0") == 0) {
    client_socket = setup_server(port);
  } else {
    client_socket = setup_client(address, port);
  }

  pthread_t send_thread, receive_thread;
  pthread_create(&send_thread, NULL, send_file, &client_socket);
  pthread_create(&receive_thread, NULL, receive_file, &client_socket);

  pthread_join(send_thread, NULL);
  pthread_join(receive_thread, NULL);

  return 0;
}