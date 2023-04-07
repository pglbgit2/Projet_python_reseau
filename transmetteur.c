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
#define SSOCKET_FILE2 "./ssocket2"

#define TRUE 1
#define FALSE 0
#define PORT 8000
#define PORT2 8490
#define PORT3 8592 
#define MAX_IFCONFIG_OUTPUT 4096
#define BUFSIZE 65536


// take a string and divide it into words
char ** parse(char * msg, int * numb, char splitter){
	char ** arg = calloc(sizeof(char *), 15);
	int n = strlen(msg);
	int j = 0;
	char * debut = msg;
	for(int i = 0; i < n; i++){
		if(msg[i] == ' ' || msg[i] == '\n' || msg[i] == splitter){
            while(msg[i] == ' ' || msg[i] == '\n'){
                i++;
            }
            i--;
			arg[j] = debut;
			j++;
			debut = msg+i+1;
			msg[i] = '\0';
		}
	}

	arg[j] = debut;
	j++;
	*numb = j;
	return arg;
}

 char ** parse_string(char * str, int * num_words) {
    char ** words = NULL;
    char * word = NULL;
    int i = 0, j = 0, n = 0;

    // Compter le nombre de mots dans la chaîne
    for (i = 0; str[i] != '\0'; i++) {
        if (str[i] == ';') {
            n++;
        }
    }
    n++; // Compter le dernier mot après la dernière virgule

    // Allouer de la mémoire pour les pointeurs de chaque mot
    words = calloc(n, sizeof(char*));
    if (words == NULL) {
        printf("Erreur: échec d'allocation de mémoire.\n");
        exit(1);
    }

    // Extraire chaque mot de la chaîne
    word = strtok(str, ";");
    while (word != NULL) {
        words[j] = word;
        j++;
        word = strtok(NULL, ";");
    }

    // Stocker le nombre total de mots
    *num_words = n;

    return words;
}

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


int update_iptable(char * port, char * ip, char *** iptables){
    int i = 0;
    while(*iptables[i] != NULL){
        i++;
    }
    port[strlen(port)] = ';';
    strcpy(*iptables[i], port);
    ip[strlen(ip)] =';';
    strcpy(*iptables[i+1], ip);
}

int put_cell(list_joueur** list, list_joueur* cell){
    if (*list == NULL){
        *list = cell;
    }
    else{
	    list_joueur * list_it = *list;
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

list_joueur * create_connect(char * port, char * ip, list_joueur ** list){
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
        printf("%d\n", new_cell->sockfd);
        //printf("debug3\n");
        if (*list != NULL){
            put_cell(list,new_cell);
        }
        else{
            *list = new_cell;
        }
        //printf("debug4\n");
	    return new_cell;
}


int sendall(char * buffer, list_joueur * player_list){
    printf("send all called\n");
    int test;
    list_joueur * list_it = player_list;
    while (list_it != NULL){
        test = send(list_it->sockfd, buffer, BUFSIZE, 0);
        if (test < 0){
            return -1;
        }
        list_it = list_it->next;
    }
    return 1;
}

char * getiptable(char ** iptable){
    char * table = calloc(sizeof(char),200);
    char * parseur = iptable[0];
    int i = 0;
    while (parseur != NULL){
        strcpy(table+strlen(table),parseur);
        table[strlen(table)] = ';';
        i++;
        parseur = iptable[i];
    }
}

char** get_iptable() {
    int nombreAdressesIP = 0; // Nombre d'adresses IP récupérées
    char** iptable = NULL; // Tableau pour stocker les adresses IP

    // Allouer de la mémoire pour le tableau iptable
    iptable = (char**)malloc(sizeof(char*));

    if (iptable == NULL) {
        perror("Erreur d'allocation de mémoire");
        exit(EXIT_FAILURE);
    }

    char* adresseIP = NULL;

    // Boucle pour récupérer les adresses IP une par une
    while ((adresseIP = my_ip_address()) != NULL) {
        // Réallouer la mémoire pour agrandir le tableau iptable
        iptable = (char**)realloc(iptable, (nombreAdressesIP + 2) * sizeof(char*)); // +2 pour le nouveau pointeur NULL de fin de tableau et l'adresse IP récupérée

        if (iptable == NULL) {
            perror("Erreur d'allocation de mémoire");
            exit(EXIT_FAILURE);
        }
        // Allouer de la mémoire pour stocker l'adresse IP récupérée
        int longueurAdresseIP = strlen(adresseIP) + 1; // +1 pour le caractère de fin de chaîne
        iptable[nombreAdressesIP] = (char*)malloc(longueurAdresseIP * sizeof(char));
        if (iptable[nombreAdressesIP] == NULL) {
            perror("Erreur d'allocation de mémoire");
            exit(EXIT_FAILURE);
        }

        // Copier l'adresse IP récupérée dans le tableau iptable
        strcpy(iptable[nombreAdressesIP], adresseIP);

        nombreAdressesIP++;

        free(adresseIP);
    }
    // Ajouter le pointeur NULL de fin de tableau
    iptable[nombreAdressesIP] = NULL;

    return iptable;
}

int my_ip_address(){ //Programme donnant l'adresse IP locale de la machine sur le réseau utilisé

    char ifconfig_output[MAX_IFCONFIG_OUTPUT];
    char *inet_address = NULL;
    char *interface_name = ""; // replace with the name of the interface you want to query

    FILE *ifconfig_pipe = popen("ifconfig", "r");

    if (ifconfig_pipe == NULL) {
        perror("popen");
        exit(EXIT_FAILURE);
    }

    while (fgets(ifconfig_output, MAX_IFCONFIG_OUTPUT, ifconfig_pipe) != NULL) {
        if (strstr(ifconfig_output, interface_name) != NULL) {
            inet_address = strtok(ifconfig_output, " \t\n");
            while (inet_address != NULL) {
                if (inet_address[0] == 'i' && inet_address[1] == 'n' && inet_address[2] == 'e' && inet_address[3] == 't') {
                    inet_address = strtok(NULL, " \t\n");
                    printf("%s\n", inet_address);
                    exit(EXIT_SUCCESS);
                }
                inet_address = strtok(NULL, " \t\n");
            }
        }
    }
    return inet_address;
}


int main(int argc, char ** argv)
{

    if (argc != 1 && argc != 3 && argc != 4){ //pour test le 4
        printf("Error: you're supposed to either give IP and Port number as arguments, or nothing\n");
        return -1;
    }

    printf("argv1: %s\n", argv[1]);
    printf("argv2: %s\n", argv[2]);

    char* buffer = calloc(sizeof(char),BUFSIZE);


    struct sockaddr_un svaddr, claddr;

    int fd, clfd, bytes, message_size, total_received;

    socklen_t clilen=sizeof(claddr);

    if((fd = socket(AF_UNIX, SOCK_STREAM, 0)) == -1) {
        stop("socket");
    }
    if (argc == 1){
        if( remove(SSOCKET_FILE) == -1 && errno != ENOENT)
        {
            stop("remove");
        }
    }
    if (argc == 3){
        if( remove(SSOCKET_FILE2) == -1 && errno != ENOENT)
        {
            stop("remove");
        }
    }

    bzero(&svaddr, sizeof(svaddr));
    svaddr.sun_family = AF_UNIX;
    if (argc == 1){
        strncpy(svaddr.sun_path, SSOCKET_FILE, sizeof(svaddr.sun_path) - 1);
    }
    if (argc == 3){
        strncpy(svaddr.sun_path, SSOCKET_FILE2, sizeof(svaddr.sun_path) - 1);
    }
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

    int bindsock, len, activity, max_sd, sd, new_socket,valread;
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
    char * port = calloc(sizeof(char),10);
    char * ip = calloc(sizeof(char),30);
    int socket_nouveau;

    if(argc == 3 || argc == 4){
        strcpy(buffer, argv[1]); // ./prog port ip
        strcpy(tamp, argv[2]);
        //printf("buffer: %s\n",buffer);
        //printf("tamp: %s\n",tamp);

        new_cell = create_connect(buffer, tamp, &list_bind);
        send(new_cell->sockfd,"#newco\n",8,0);
        return -1;
        // send(new_cell->sockfd,"?askfortip",11,0);
        // bzero(buffer,BUFSIZE);
        // if(recv(new_cell->sockfd,buffer,BUFSIZE,0) < 0){
        //     printf("error recv connect\n");
        // }
        // iptables = parse(buffer,0,';');
        // char * parseur = iptables[0];
        // int i = 0;
        // while (parseur != NULL){
        //     bzero(buffer,strlen(buffer));
        //     bzero(tamp,strlen(tamp));

        //     i++;
        //     parseur = iptables[i];
        //     strcpy(buffer,parseur);

        //     i++;
        //     parseur = iptables[i];
        //     strcpy(tamp,parseur);

        //     create_connect(buffer, tamp, &list_bind);
        // }
        // list_it = list_bind;
        // bzero(buffer,strlen(buffer));
        // strcpy(buffer,"?heremyip: MY PORT ; MY IP ;");
        // while (list_it != NULL){
        //     send(list_it->sockfd,buffer,strlen(buffer),0);
        //     list_it = list_it->next;
        // }


        // faire une fonction char** getiptables()
        // et du coup on appelle create_connect pour chaque ip/port dans iptables
        // faut envoyer son port (le port sur lequel notre socket bindée écoute), son ip (127.0.0.1 pour les test) avec la socket de new_cell avec un truc du style: '?voilamonip?ip?port'
        // du coup on aura besoin ici de la fonction de shériff pour récupérer l'ip 

        // il y a deux listes: list contient la liste des sockets sur lesquelles on écoute
        // liste_bind contient la liste des socket sur les quelles on envoie (et du coup l'autre écoute dessus de l'autre coté)
    }
    //strncpy(buffer,"#newco\ntoto",12);
    // if(send(clfd, buffer, strlen(buffer), 0)<0)
    // {
    //     stop("send python");
    // }
    // else
    // {
    //     printf("sent %s\n", buffer);
    // }
    //printf("avant le while\n");
    // message_size = strlen(buffer);
    // printf("envoi à Python\n");
    // if(send(clfd,&message_size, sizeof(message_size), 0)==-1)
    // {
    // stop("send size to Python");
    // }
    
    // // envoie message à Python
    // if((send(clfd, buffer, message_size, 0))==-1)
    // {
    // stop("send to Python");
    // }
    while(TRUE) 
    {
        printf("dans le while\n");
        FD_ZERO(&readfds);
        FD_SET(bindsock, &readfds);
        FD_SET(clfd, &readfds);

        // penser à cet la socket de l'api
        max_sd = bindsock;
        list_it = list;
        printf("test1\n");

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
        printf("test2\n");
        activity = select( max_sd+1 , &readfds , NULL , NULL , NULL);
        printf("test3\n");

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
                if (list != NULL){
                    put_cell(&list, new_cell);
                }
                else{
                    list = new_cell;
                }
            }
        }
        
        else
        {
            list_it = list;
            printf("la bas\n");

            while( list_it != NULL) 
            {
                sd = list_it->sockfd;
                if (FD_ISSET( sd , &readfds)) 
                {
                    bzero(buffer, BUFSIZE);
                    if ((valread = recv( sd , buffer, 65536, 0)) == 0) // à sécuriser
                    {
                        //cas de deconnection 
                        getpeername(sd , (struct sockaddr*)&address , (socklen_t*)&len);
                        remove_cell(&list, list_it);
                    }
                    else
                    {
                        printf("%s\n",buffer);
                       if(buffer[0] == '?'){
                            if (strncmp(buffer,"?askfortip",10) == 0){
                                tamp = getiptable(iptables);
                                send(sd,tamp,strlen(tamp),0);
                            }

                            if (strncmp(buffer,"?heremyip:",10) == 0){
                                bzero(tamp,strlen(tamp));
                                strcpy(tamp,buffer+10);
                                

                                int i = 0;
                                while(tamp[i] != ';')
                                    port[i] = tamp[i];
                                i++;
                                while(tamp[i] != ';')
                                    ip[i] = tamp[i];
                                update_iptable(port,ip,&iptables); // elle existe pas encore
                                create_connect(port,ip,&list_bind);
                            }
                       }


                       
                        // liste des cas possibles
                        // on peut se servir d'un cas ici genre si le buffer contient '?askforip?' l'autre renvoie iptables, avec sa propre ip dedans, et il faut les ports aussi
                        // cas de reception ip du coup : l'autre nous indique simplement quel est son ip
                        // c'est important de faire la distinction entre les deux precedents, parce que:
                        // on demande une fois la liste des addresse ip, mais on doit indiquer son ip /port à chaque joueur
                        // quand on recoit une addresse ip et un port, il faut appeller create_connect dessus

                        // cas commence par '?' : message destiné à C (juste du c vers c)
                        // cas commence par '#' : message destiné à python
                        if (buffer[0]=='#')
                        {
                            //envoi taille à python
                            if (strncmp(buffer,"#newco",6) == 0){
                                printf("nouveau\n");
                            }
                            message_size = strlen(buffer);
                            printf("envoi à Python\n");
                            if(send(clfd,&message_size, sizeof(message_size), 0)==-1)
                            {
                                stop("send size to Python");
                            }
                            printf("buffer a envoyer a python:%s\n",buffer);
                            //envoie message à Python
                            if((send(clfd, buffer, message_size, 0))==-1)
                            {
                                stop("send to Python");
                            }
                            return -1;
                        }

                        // aucun des deux precedents: erreurs 





                    }
                }
                list_it = list_it->next;
                printf("test while\n");
            }

            printf("ici\n");

            //API
            if(FD_ISSET( clfd , &readfds))
            {
                bzero(buffer, sizeof(buffer));

                //recevoir taille message
                printf("attente réception...\n");
                if((received = recv(clfd, &message_size, sizeof(int), MSG_WAITALL))!=sizeof(int))
                {
                    stop("recv size");
                }
                else
                {
                    printf("%i\n", message_size);
                }

                //reception message
                received = recv(clfd, buffer, message_size, MSG_WAITALL);
                if(received==-1)
                {
                    stop("recv msg");
                    continue;
                }
                else
                {
                    puts("received from Python");                
                    printf("%s\n",buffer);
                    printf("%c\n",buffer[0]);
                    if (buffer[0] == '#' && list_bind != NULL){
                        sendall(buffer,list_bind);
                    }
                    printf("jspsqyspasse\n");
                    list_it = list_bind;
                    printf("avant affichage list_bind\n");
                    
                    //envoie des données en broadcast
                    // TODO
                }
            }
                
        }
        
        
    }


    return EXIT_SUCCESS;
}
