#include <stdio.h>
#include <stdlib.h>
#include <string.h>
struct log
{
    char command[10];
    char path1[4096];
    char path2[4096];
    char ip1[100];
    int port1;
    char ip2[100];
    int port2;
    int status; // 0 -> failed , 1-> successfull but after ss failure and 2-> completely successfull
    char ack[4096];
    int index_in_array_of_listed_SS;
    struct log *next;
};
typedef struct log *log;
void addtolog(log head, int index, char *command, char *path1, char *path2, char *ip1, char *ip2, int port1, int port2,int status,char* ACK);
