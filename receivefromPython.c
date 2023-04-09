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
#include <sys/select.h>
#include <math.h>

#define BUFSIZE 65536
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

    char buffer[BUFSIZE];
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
    strncpy(buffer,"#newco\ntoto",12);
        if(send(clfd, buffer, strlen(buffer), 0)<0)
        {
            stop("send python");
        }
        else
        {
            printf("sent %s\n", buffer);
        }
    fd_set readfds;
    int max_sd, activity;
    while(1)
    {   
        FD_ZERO(&readfds);
        FD_SET(clfd, &readfds);
        max_sd = clfd;
        activity = select(max_sd+1,&readfds,NULL,NULL,NULL);
        if ((activity < 0) && (errno != EINTR)) 
        {
            stop("select error");
        }
        if (FD_ISSET(clfd, &readfds))
        {
            bzero(&buffer, sizeof(buffer));
            if((received = recv(clfd, buffer, BUFSIZE-1, 0)==-1))
            {
                stop("recv");
                continue;
            }
            else
            {
                puts("received from Python");
                printf("%s\n",buffer);
                //envoie des données en broadcast
                // TODO
            }
        }

        bzero(&buffer, sizeof(buffer));
        //réception des données des autres 
                
    }

    close(fd);
    return 0;
}

