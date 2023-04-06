#include <stdio.h>
#include <string.h>   
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>   
#include <arpa/inet.h>    
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/time.h> 
#include <sys/select.h>
#include <strings.h>
#include <sys/un.h>

#define SSOCKET_FILE "./ssocket"
#define TRUE 1
#define FALSE 0
#define PORT 8000
#define PORT2 8490
#define PORT3 8592

#define BUFSIZE 8000


int stop(char * err)
{
    perror(err);
    return -1;
}


typedef struct joueur_cell{
	int sockfd;
	struct sockaddr_in cliaddr;
	struct joueur_cell* next;
}list_joueur;



list_joueur * create_cell(int* sockfd, struct sockaddr_in* addr){
	list_joueur* l = calloc(sizeof(list_joueur),1);
	l->next = NULL;

    if(sockfd != NULL){
	    l->sockfd = *sockfd;
    }
    if(addr != NULL){
	    bzero(&l->cliaddr, sizeof(struct sockaddr_in));
	    l->cliaddr = *addr;
    }
    if(sockfd != NULL){
    int z;
	struct linger so_linger;
	so_linger.l_onoff = TRUE;
	so_linger.l_linger = 30;
	z = setsockopt(l->sockfd, SOL_SOCKET, SO_LINGER, &so_linger, sizeof(so_linger));
	if(z){
	    printf("ERROR: setsockopt(2) (quick close case)");
        return NULL;
	}
    }
	return l;
}



int put_cell(list_joueur* list, list_joueur* cell){
    if (list == NULL){
        list = cell;
    }
    else{
	    list_joueur * list_it = list;
	    while(list_it->next != NULL){
		    if(list_it == cell){
			return 0;
		    }
		    list_it = list_it->next;
	    }
	    list_it->next = cell;
    }
    return 1;
}

int remove_cell(list_joueur** adlist, list_joueur* cell){
    if(*adlist == NULL){
        return 0;
    }
    if(*adlist == cell){
        
       if(cell->next == NULL){
            close(cell->sockfd);
            free(cell);
            *adlist = NULL;
            return 1;
       }
       if(cell->next != NULL){
            *adlist = (list_joueur*) cell->next;
            close(cell->sockfd);
            free(cell);
            return 1;
       }
    }
    list_joueur * list_it = *adlist;

	while(list_it->next != NULL){
		if(list_it->next == (struct joueur_cell*)cell){
            list_joueur* destroy = (list_joueur*) list_it->next;
            list_it->next = list_it->next->next;
            close(destroy->sockfd);
            free(destroy);
            return 1;
        }
        list_it = list_it->next;
	}
    return 0;
}

list_joueur * create_connect(char * port, char * ip, list_joueur * list){
        int sockfd;
	    struct sockaddr_in first;
	    sockfd = socket(AF_INET , SOCK_STREAM , 0);
	    if (sockfd == -1)
	    {
		    stop("ERROR socket creation");
            return NULL;
	    }
	    //printf("Socket created\n");
	    first.sin_addr.s_addr = inet_addr(ip);
	    first.sin_family = AF_INET;
	    first.sin_port = htons(atoi(port));
        //printf("debug\n");

	    if (connect(sockfd , (struct sockaddr *)&first , sizeof(first)) < 0)
	    {
		    stop("connect error");
            return NULL;
	    }

        //printf("Connected\n");
        list_joueur * new_cell;
        //printf("debug2\n");

        new_cell = create_cell(&sockfd,&first);
        //printf("debug3\n");
        put_cell(list,new_cell);
        //printf("debug4\n");
	    return new_cell;
}



int main(int argc, char ** argv)
{

    if (argc != 1 && argc != 3 && argc != 4){ //pour test le 4
        printf("Error: you're supposed to either give IP and Port number as arguments, or nothing\n");
        return -1;
    }


    int bindsock, len, activity, max_sd, sd, new_socket,valread;
    char* buffer = calloc(sizeof(char),BUFSIZE+5);
    struct sockaddr_in address;
    struct sockaddr_in jaddr;
    int opt = TRUE;
    fd_set readfds;
    if( (bindsock = socket(AF_INET , SOCK_STREAM , 0)) == 0) 
    {
        stop("ERROR: socket creation");
        return -1;
    }
    printf("socket ok\n");

    if( setsockopt(bindsock, SOL_SOCKET, SO_REUSEADDR, (char *)&opt, sizeof(opt)) < 0 )
    {
        stop("ERROR: setsockopt");
        return -1;
    }
    printf("setsockopt ok\n");
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = inet_addr( "127.0.0.1" );
    
    // c'est juste pour tester sur un seul ordi, pour le troisieme, utiliser un troisieme argument random
    if (argc == 3){
        address.sin_port = htons( PORT2 );
    }
    if (argc == 1){
        address.sin_port = htons( PORT );
    }
    if (argc == 4){
        address.sin_port = htons( PORT3 );
    }

    if (bind(bindsock, (struct sockaddr *)&address, sizeof(address))<0) 
    {
        stop("ERROR binding socket");
         return -1;
    }
	printf("binding ok\n");

    if (listen(bindsock, 3) < 0)
    {
        stop("ERROR set listening");
        return -1;
    }
    printf("listen ok\n");
    len = sizeof(address);
    char * tamp = calloc(sizeof(char),BUFSIZE+25);
    list_joueur * list = NULL;
    list_joueur * list_it = list;
    list_joueur * new_cell = NULL;
    list_joueur * list_bind = NULL;
    char ** iptables;

    if(argc == 3 || argc == 4){
        strcpy(buffer, argv[1]); // ./prog port ip
        strcpy(tamp, argv[2]);
        //printf("buffer: %s\n",buffer);
        //printf("tamp: %s\n",tamp);

        new_cell = create_connect(buffer, tamp, list_bind);
        // faire une fonction char** getiptables()
        // faire une fonction update_iptable()
        // et du coup on appelle create_connect pour chaque ip dans iptables
        // faut envoyer son port, son ip avec la socket de new_cell avec un truc du style: '?voilamonip?ip?port'
        // du coup on aura besoin ici de la fonction de shériff pour récupérer l'ip 

        // il y a deux listes: list contient la liste des sockets sur lesquelles on écoute
        // liste_bind contient la liste des socket sur les quelles on envoie (et du coup l'autre écoute dessus de l'autre coté)
    }
    //printf("avant le while\n");
    while(TRUE) 
    {
        //printf("dans le while\n");
        FD_ZERO(&readfds);
        FD_SET(bindsock, &readfds);
        // penser à cet la socket de l'api
        max_sd = bindsock;
        list_it = list;
        //printf("test1\n");

        while( list_it != NULL) 
        {
            //printf("toto\n");
		    sd = list_it->sockfd;
			if(sd > 0){
				FD_SET( sd , &readfds);
            }
            if(sd > max_sd){
				max_sd = sd;
            }
            list_it = list_it->next;
        }
        //printf("test2\n");
        activity = select( max_sd+1 , &readfds , NULL , NULL , NULL);
        //printf("test3\n");

        if ((activity < 0) && (errno != EINTR)) 
        {
            stop("select error");
            return -1;
        }
        if (FD_ISSET(bindsock, &readfds)) 
        {
            if ((new_socket = accept(bindsock, (struct sockaddr *)&jaddr, (socklen_t*)&len))<0)
            {
                stop("accept");
                return -1;
            }
            printf("new joueur\n");
            new_cell = create_cell(&new_socket, &jaddr);
            if(new_cell == NULL){
                stop("ERROR create cell");
                return -1;
            }

            if(list == NULL){
                list = new_cell;
            }
            else{
                put_cell(list, new_cell);
            }
        }
        
        else{
            list_it = list;
            while( list_it != NULL) 
            {
                sd = list_it->sockfd;
                if (FD_ISSET( sd , &readfds)) 
                {
                    bzero(buffer, BUFSIZE);
                    if ((valread = recv( sd , buffer, 1024, MSG_DONTWAIT)) == 0)
                    {
                        //cas de deconnection 
                        getpeername(sd , (struct sockaddr*)&address , (socklen_t*)&len);
                        remove_cell(&list, list_it);
                    }
                    else
                    {
                        // liste des cas possibles
                        // on peut se servir d'un cas ici genre si le buffer contient '?askforip?' l'autre renvoie iptables, avec sa propre ip dedans
                        // cas de reception ip du coup 



                        // cas commence par '?' : message destiné à C (c vers c)
                        // cas commence par '#' : message destiné à python
                        // aucun des deux precedents: erreurs 


                    }
                }
                list_it = list_it->next;
            }
        }
        // rajouter API en C ici 
    }


    return EXIT_SUCCESS;
}
