//
// Created by agran on 25/03/2023.
//
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

#define SOCKET_FILE "./"

void stop(char * err)
{
    perror(err);
    exit(EXIT_FAILURE);
}

int main(int argc, char ** argv)
{
    struct sockaddr_un addr;
    char buffer[1024];
    int fd, bytes_read;

    if((fd = socket(AF_UNIX, SOCK_STREAM, 0)) == -1) {
        stop(socket);
    }

    bzero(&addr, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_family, SOCKET_FILE, sizeof(addr.sun_path)-1);

    if (connect(fd, (struct sockaddr *)&addr, sizeof(addr)) == -1){
        stop("connect");
    }

    while((bytes = recv(fd, buffer, sizeof(buffer), 0)) > 0) {
        printf("reçu : %s", bytes, buffer);
    }

    if ((bytes == -1)){
        stop("recv";)
    }

    close(fd;)

    return 0;
}

