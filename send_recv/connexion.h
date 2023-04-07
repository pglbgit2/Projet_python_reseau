#ifndef CONNEXION_H
#define CONNEXION_H

void *send_file(void *arg);
void *receive_file(void *arg);
int setup_server(int port);
int setup_client(const char *address, int port);

#endif
