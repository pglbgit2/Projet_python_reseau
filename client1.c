#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define BUFLEN 512 // longueur du tampon
#define PORT 1234  // port de destination

void stop(char *s)
{
    perror(s);
    exit(1);
}

int main(int argc, char *argv[])
{
    int sockfd;
    char message[BUFLEN + 1];
    struct sockaddr_in sockaddr;
    struct sockaddr_in peeraddr;
    socklen_t peerlen;

    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        stop("socket");
    }

    sockaddr.sin_family = AF_INET;
    sockaddr.sin_addr.s_addr = INADDR_ANY;
    sockaddr.sin_port = htons(PORT);

    if (bind(sockfd, (struct sockaddr *)&sockaddr, sizeof(sockaddr)) == -1)
    {
        stop("bind");
    }

    if (listen(sockfd, 1) == -1)
    {
        stop("listen");
    }

    printf("Waiting for incoming connection...\n");

    peerlen = sizeof(peeraddr);
    int newsockfd = accept(sockfd, (struct sockaddr *)&peeraddr, &peerlen);

    if (newsockfd == -1)
    {
        stop("accept");
    }

    printf("Connected with peer: %s:%d\n", inet_ntoa(peeraddr.sin_addr), ntohs(peeraddr.sin_port));

    for (int i = 0; i < 26; i++)
    {
        //send the message
        memset(&message, 'A' + i, BUFLEN);
        message[BUFLEN - 1] = '\0';
        printf("Send %s\n", message);
        if (sendto(newsockfd, message, strlen(message), 0, (struct sockaddr *)&peeraddr, sizeof(peeraddr)) == -1)
        {
            stop("sendto");
        }

        // recv
        bzero(&message, BUFLEN + 1);
        if (recvfrom(newsockfd, message, BUFLEN, 0, (struct sockaddr *)&peeraddr, &peerlen) < 0)
        {
            stop("recvfrom");
        }
        printf("Recv : %s\n", message);
    }

    close(newsockfd);
    close(sockfd);
    return 0;
}
