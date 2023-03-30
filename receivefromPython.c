//
// Created by agran on 25/03/2023.
//
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>
#include <errno.h>
#include <strings.h>
#include <string.h>


#define SSOCKET_FILE "./ssocket"
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

    int clilen=sizeof(claddr);

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

    bzero(&claddr, sizeof(claddr));


    if (listen(fd, 1) != 0){
        stop("listen");
    }
    else{
        printf("listening\n");
    }

    clfd = accept(fd, (struct sockaddr *)&claddr, &clilen);
    printf("accepted\n");
    printf("%i\n", claddr.sun_family);
    int received = 0;
    while(1)
    {
        bzero(&buffer, sizeof(buffer));
        // if((received = recv(clfd, buffer, BUFSIZ, 0))==-1)
        // {
        //     stop("recv");
        //     continue;
        // }
        // else if (received == 0) continue;
        // else
        // {
        //     puts("received from Python");
        //     printf("%s\n",buffer);

        //     //envoie des données en broadcast
        //     //TODO
        // }

        bzero(&buffer, sizeof(buffer));
        //réception des données des autres 
        
        //TODO
        printf("TEST\n");
        //et envoie au programme Python
        strncpy(buffer,"#newco\ntoto",12);
        if(send(clfd, buffer, strlen(buffer), 0)<0)
        {
            stop("send python");
        }
        sleep(1);
        
    }

    close(fd);
    return 0;
}

