#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/socket.h>
#include <strings.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <unistd.h>
#include <netdb.h>
#include <string.h>
#include <errno.h>

#define PORT 8888

void *send_file(void *arg);
void *recv_file(void *arg);
void *initialise(void *arg);
void *wait_connexion(void *arg);

typedef struct joueur{

        int sockfd;
        char *ip_address_;
} *joueur;

char input[10];
int *result1;
int *result2;

int main()
{

    while(1){

        pthread_t thread_id_1, thread_id_2, thread_id_3, thread_id_4;
        int rc1, rc2, rc3, rc4;

        // Create thread 1 for sending files
        rc1 = pthread_create(&thread_id_1, NULL, send_file, NULL);
        if (rc1) {
            printf("Error: could not create thread 1\n");
            exit(-1);
        }

        // Create thread 2 for receiving files
        rc2 = pthread_create(&thread_id_2, NULL, recv_file, NULL);
        if (rc2) {
            printf("Error: could not create thread 2\n");
            exit(-1);
        }
        // Create thread 3 to initialise a connection
        rc3 = pthread_create(&thread_id_3, NULL, initialise, NULL);
        if (rc3) {
            printf("Error: could not create thread 3\n");
            exit(-1);
        }
        // Create thread 4 to wait an incoming connection
        rc4 = pthread_create(&thread_id_4, NULL, wait_connexion, NULL);
        if (rc4) {
            printf("Error: could not create thread 4\n");
            exit(-1);
        }
    
        fgets(input, 10, stdin);
    

        // Wait for threads to finish
        pthread_join(thread_id_3,  (void **)&result1);
        pthread_join(thread_id_4,  (void **)&result2);
        pthread_join(thread_id_1, NULL);
        pthread_join(thread_id_2, NULL);
        
        printf("Valeur du thread initialise: %d\n", result1);
        printf("Valeur du thread wait: %d\n", result2);++
    
  
    }

    return 0;
}

void *send_file(void *arg)
{
    
        if (strcmp(input, "1\n") == 0) {
            printf("Bonjour du send\n");
            //break;
       
        } else {
            printf("Je ne comprends pas du send\n");
            //break;
        }
    
}

void *recv_file(void *arg)
{
   
        if (strcmp(input, "2\n") == 0) {
            printf("Bonjour du recv\n");
            //break;
     
        } else {
            printf("Je ne comprends pas du recv\n");
            //break;
        }
    
}

void *initialise(void *arg){


    while(1){

        if (strcmp(input, "initialise\n") == 0) {
            joueur jo;  //joueur voulant rejoindre la partie en cours

            jo = calloc(1, sizeof(struct joueur));
            jo->ip_address_ = calloc(1, sizeof(struct joueur));
            //jo->ip_address_= my_ip_address();

            struct sockaddr_in server;
            char buff[64000];
            
            //Create socket
            jo->sockfd = socket(AF_INET , SOCK_STREAM , 0);
            if (jo->sockfd == -1)
            {
                printf("Could not create socket");
                exit(0);
            }
            puts("Socket created");
            
            server.sin_addr.s_addr = inet_addr("127.0.0.1");
            server.sin_family = AF_INET;
            server.sin_port = htons( PORT );

            if (server.sin_addr.s_addr == INADDR_NONE) {
                printf("Invalid IP address\n");
                exit(1);
            }


            //Connect to remote server
            if (connect(jo->sockfd , (struct sockaddr *)&server , sizeof(server)) < 0)
            {
                perror("connect failed. Error");
                exit(1);
            }
            //printf("Your IP_adress is: %s\n", my_ip_address());
            puts("Connected\n");
            pthread_exit(1);

        }else{ break; }
    }
}


void *wait_connexion(void *arg){

    while(1){

        if (strcmp(input, "wait\n") == 0) {
            joueur j;  //premier joueur à commencer une partie
            joueur new_joueur;
            j = calloc(1, sizeof(struct joueur));
            new_joueur = calloc(1, sizeof(struct joueur));
            new_joueur->sockfd = 0;
            
            int c , read_size, sd;
            struct sockaddr_in server , client;
            
            //Create socket
            j->sockfd = socket(AF_INET , SOCK_STREAM , 0);
            if (j->sockfd == -1)
            {
                printf("Could not create socket");
            }
            puts("Socket created");
            
            //Prepare the sockaddr_in structure
            server.sin_family = AF_INET;
            server.sin_addr.s_addr = INADDR_ANY;
            server.sin_port = htons(PORT);
            
            //Bind
            if( bind(j->sockfd,(struct sockaddr *)&server , sizeof(server)) < 0)
            {
                //print the error message
                perror("bind failed. Error");
                exit(1);
            }
            puts("bind done");
            

            //Listen to new incoming connections
            if(listen(j->sockfd, 3)<0){
                perror("listen");exit(EXIT_FAILURE);
            }
            
            //Accept and incoming connection
            puts("Waiting for incoming connections...");
            c = sizeof(struct sockaddr_in);
            if(((new_joueur->sockfd) = accept(j->sockfd,(struct sockaddr*)&client,
                    (socklen_t *)&c))<0){
                        perror("accept");
                        exit(EXIT_FAILURE);
                    }

                    //informations de la socket
                    printf("New connection, socket fd: %d\n ip : %s\n port %d\n",
                    new_joueur->sockfd, inet_ntoa(client.sin_addr), ntohs(client.sin_port));
                    pthread_exit(1);
                    break;
                   

        }else{ break; }
    }
}