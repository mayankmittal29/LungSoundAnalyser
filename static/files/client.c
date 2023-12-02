#include"header.h"






  int client_socket;
int client_id;
void send_request(int socket,  MsgToNM *packet)
{
   send(socket, packet, sizeof(MsgToNM), 0);
}
void send_request_SS(int socket,  MsgToSS *packet)
{
   send(socket, packet, sizeof(MsgToSS), 0);
}
 


void ctrlC_Handler(int signal) {
    printf("Ctrl+C pressed. Closing Sockets... Exiting...\n");
    close(client_socket);
    exit(0);
}
int main()
{
    signal(SIGINT, ctrlC_Handler);

   struct sockaddr_in server_address;


   // Create socket
   client_socket = socket(AF_INET, SOCK_STREAM, 0);
   if (client_socket == -1)
   {
       perror("Socket creation failed");
       exit(1);
   }


   server_address.sin_family = AF_INET;
   server_address.sin_port = htons(NM_PORT);
   server_address.sin_addr.s_addr = inet_addr(NM_IP);


  //  Connect to the Naming Server
   if (connect(client_socket, (struct sockaddr *)&server_address, sizeof(server_address)) == -1)
   {
       perror("Connection to Naming Server failed");
       exit(1);
   }
   printf("Enter clientID");
   scanf("%d",&client_id);

char use[100];
fgets(use, 100, stdin);

while(1){
   char *request = (char *)malloc(sizeof(char) * 4096);


   // Take user input for the request
   printf("Enter your command: ");
   fgets(request, 4096, stdin);


   // Remove the newline character from the input
   size_t len = strlen(request);
   if (len > 0 && request[len - 1] == '\n')
   {
    
       request[len - 1] = '\0';
   }
    MsgToNM *packet;
   packet=(MsgToNM*)malloc(sizeof(MsgToNM));
    strcpy(packet->command, request);
    packet->FromID=client_id;
    char * request2;
    char *request4;
    char *request3;
char *request1 = (char *)malloc(sizeof(char) * 4096);
 if(strcmp("COPY",packet->command)!=0)
 {
     printf("Enter your path: ");
   fgets(request1, 4096, stdin);
    strcpy(packet->path, request1);
 }
   packet->From='C';
   if(strcmp("WRITE",packet->command)==0)
   {
request2 = (char *)malloc(sizeof(char) * 4096);

     printf("Enter your data: ");
   fgets(request2, 4096, stdin);
    len = strlen(request2);
   if (len > 0 && request2[len - 1] == '\n')
   {
    
       request2[len - 1] = '\0';
   }
    //  printf("%s %s %s\n ",packet->command,packet->path,request2);
// copy the write command content
   }
   if(strcmp("COPY",packet->command)==0)
   {
    request3 = (char *)malloc(sizeof(char) * 4096);

     printf("Enter your path1: ");
   fgets(request3, 4096, stdin);
    len = strlen(request3);
   if (len > 0 && request3[len - 1] == '\n')
   {
    
       request3[len - 1] = '\0';
   }
   request4 = (char *)malloc(sizeof(char) * 4096);

     printf("Enter your path2: ");
   fgets(request4, 4096, stdin);
    size_t len = strlen(request4);
   if (len > 0 && request4[len - 1] == '\n')
   {
    
       request4[len - 1] = '\0';
   }
   // copy the copy content
   

   }
 
   send_request(client_socket, packet);
   if ((strcmp(packet->command, "READ") == 0) || (strcmp(packet->command, "WRITE") == 0) || (strcmp(packet->command, "LS") == 0) || (strcmp(packet->command, "INFO") == 0))
   {
       struct  MsgToCLIENT *servercom;
       servercom=(MsgToCLIENT*)malloc(sizeof(MsgToCLIENT));
    //    servercom->ip = (char *)malloc(sizeof(char) * 16);
       int info_received = recv(client_socket, servercom, sizeof(MsgToCLIENT), 0);
       if (info_received > 0)
       {
        printf("%s\n",servercom->ip);
           int ss_socket = socket(AF_INET, SOCK_STREAM, 0);
           struct sockaddr_in ss_address;
           ss_address.sin_family = AF_INET;
           ss_address.sin_port = htons(servercom->port_SS);
           ss_address.sin_addr.s_addr = inet_addr(servercom->ip);


           // Connect to the Storage Server
           if (connect(ss_socket, (struct sockaddr *)&ss_address, sizeof(ss_address)) == -1)
           {
               perror("Connection to Storage Server failed");
               exit(1);
           }
           MsgToSS* message;
           message=(MsgToSS*)malloc(sizeof(MsgToSS));
           strcpy(message->Command,packet->command);
           strcpy(message->path,packet->path);
           strcpy(message->To_write,request2);
           send_request_SS(client_socket,message);
            MsgToCLIENT* ss_response;
            ss_response=(MsgToCLIENT*)malloc(sizeof(MsgToCLIENT));
           int response_received = recv(ss_socket, ss_response, sizeof(MsgToCLIENT), 0);
           if (response_received > 0)
           {
               
               printf("Received response from Storage Server: %s\n", ss_response->Result);
           }
           close(ss_socket);
       }
   }
   else
   {
       MsgToCLIENT* response;
       response=(MsgToCLIENT*)malloc(sizeof(MsgToCLIENT));
       int bytes_received = recv(client_socket, response, sizeof(MsgToCLIENT), 0);
       if (bytes_received > 0)
       {
           if(response->Ack==1)
           printf("Operation done successfully...\n");
        //    printf("Received response from Naming Server: %s\n", response);
            else 
            {
                printf("The command did not execute successfully\n");
            }
       }
   }
}
   close(client_socket);


   return 0;
}
