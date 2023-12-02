#include <stdio.h>
#include <stdlib.h>
#include <string.h>
struct node
{
    char command[10];
    char path1[4096];
    char path2[4096];
    char ip1[100];
    int port1;
    char ip2[100];
    int port2;
    struct node *next;
};
typedef struct node *node;
struct store
{
    char ip1[100];
    int port1;
    char ip2[100];
    int port2;
};
typedef struct store* store;
store search(char *command, char *path1, char *path2, node head, store packet);
void addtolistof20(node head, int exist, char *command, char *path1, char *path2, char *ip1, char *ip2, int port1, int port2);
