//
// Created by agran on 25/03/2023.
//
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>
#include <errno.h>

#define SSOCKET_FILE "./sscocket"
#define CSOCKET_FILE "./csocket"

void stop(char * err)
{
    perror(err);
    exit(EXIT_FAILURE);
}

int main(int argc, char ** argv)
{
    struct sockaddr_un svaddr, claddr;
    char buffer[BUFSIZ];
    int fd, clfd, bytes;

    if((fd = socket(AF_UNIX, SOCK_STREAM, 0)) == -1) {
        stop("socket");
    }

    if(remove(SSOCKET_FILE) == -1 && errno != ENOENT)
    {
        stop("remove");
    }

    bzero(&svaddr, sizeof(svaddr));
    svaddr.sun_family = AF_UNIX;
    strncpy(svaddr.sun_path, SSOCKET_FILE, sizeof(svaddr.sun_path) - 1);

    if (bind(fd, (struct sockaddr *)&svaddr, sizeof(svaddr)) == -1){
        stop("binding");
    }

    /*bzero(&claddr, sizeof(claddr));
    claddr.sun_family = AF_UNIX;
    strncpy(claddr.sun_path, CSOCKET_FILE, sizeof(claddr.sun_path) - 1);*/

    if (listen(fd, 1) != 0){
        stop("listen");
    }
    else{
        printf("listening\n");
    }

    clfd = accept(fd, &claddr, sizeof(claddr));

    while(1)
    {
        if(recv(fd, buffer, BUFSIZ, 0)==-1)
        {
            stop("recv");
        }
        else
        {
            puts("received from Python");
            printf(bytes);

            //envoie des données en broadcast
        }


        //réception des données des autres et envoie au programme Python

    }

    close(fd);

    return 0;
}

