#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define BUFLEN 512 // longueur du tampon
#define PORT 1234 // port de destination

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
sockaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
sockaddr.sin_port = htons(PORT);

if (connect(sockfd, (struct sockaddr *)&sockaddr, sizeof(sockaddr)) == -1)
{
    stop("connect");
}

printf("Connected to peer %s:%d\n", inet_ntoa(sockaddr.sin_addr), ntohs(sockaddr.sin_port));

for (int i = 0; i < 26; i++)
{
    //recv
    bzero(&message, BUFLEN + 1);
    if (recvfrom(sockfd, message, BUFLEN, 0, (struct sockaddr *)&peeraddr, &peerlen) < 0)
    {
        stop("recvfrom");
    }
    printf("Recv : %s\n", message);

    // send the message
    memset(&message, 'a' + i, BUFLEN);
    message[BUFLEN - 1] = '\0';
    printf("Send %s\n", message);
    if (sendto(sockfd, message, strlen(message), 0, (struct sockaddr *)&peeraddr, sizeof(peeraddr)) == -1)
    {
        stop("sendto");
    }
}

close(sockfd);
return 0;
}