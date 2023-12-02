#include "lru.h"
void addtolistof20(node head, int exist, char *command, char *path1, char *path2, char *ip1, char *ip2, int port1, int port2)
{
    if (exist == 0) // not present in cache list
    {
        if (head == NULL) // empty list
        {
            node temp = (node)malloc(sizeof(struct node));
            strcpy(temp->command, command);
            strcpy(temp->ip1, ip1);
            strcpy(temp->ip2, ip2);
            strcpy(temp->path1, path1);
            strcpy(temp->path2, path2);
            temp->port1 = port1;
            temp->port2 = port2;
            temp->next = NULL;
            head = temp;
        }
        else
        {
            int num = 0; // number of nodes in cache list
            node start = head;
            while (start != NULL)
            {
                num++;
                start = start->next;
            }
            if (num < 20)
            {
                node temp = (node)malloc(sizeof(struct node));
                strcpy(temp->command, command);
                strcpy(temp->ip1, ip1);
                strcpy(temp->ip2, ip2);
                strcpy(temp->path1, path1);
                strcpy(temp->path2, path2);
                temp->port1 = port1;
                temp->port2 = port2;
                temp->next = head;
                head = temp;
            }
            else if (num == 20)
            {
                node temp = (node)malloc(sizeof(struct node));
                strcpy(temp->command, command);
                strcpy(temp->ip1, ip1);
                strcpy(temp->ip2, ip2);
                strcpy(temp->path1, path1);
                strcpy(temp->path2, path2);
                temp->port1 = port1;
                temp->port2 = port2;
                node end = head;
                node secondlastend = head;
                while (secondlastend->next->next != NULL)
                {
                    secondlastend = secondlastend->next;
                }
                while (end->next != NULL)
                {
                    end = end->next;
                }
                free(end);
                end = NULL;
                secondlastend->next = NULL; // removed from last
                temp->next = head;
                head = temp;
            }
        }
    }
    else // present in cache list
    {
        int index = 1;
        node cur = head;
        while (cur != NULL)
        {
            if ((strcmp(cur->command, command) == 0) && (strcmp(cur->path1, path1) == 0) && (strcmp(cur->path2, path2) == 0) && (strcmp(cur->ip1, ip1) == 0) && (strcmp(cur->ip2, ip2) == 0) && (cur->port1 == port1) && (cur->port2 == port2))
            {
                break;
            }
            else
            {
                index++;
                cur=cur->next;
            }
        }
        if(index!=1)
        {
            node prev=head;
            node cur=head;
            int i=1;
            while(i!=index)
            {
                prev=cur;
                cur=cur->next;
                i++;
            }
            prev->next=cur->next;
            cur->next=head;
            head=cur;
        }
    }
    return;
}
store search(char *command, char *path1, char *path2, node head, store packet)
{
    if (head == NULL)
    {
        return NULL;
    }
    else
    {
        int flag = 0;
        node start = head;
        while (start != NULL)
        {
            if (strcmp(command, "COPY") == 0)
            {
                if ((strcmp(start->command, command) == 0) && (strcmp(start->path1, path1) == 0) && (strcmp(start->path2, path2) == 0))
                {
                    packet->port1 = start->port1;
                    packet->port2 = start->port2;
                    strcpy(packet->ip1, start->ip1);
                    strcpy(packet->ip2, start->ip2);
                    flag = 1;
                    break;
                }
            }
            else
            {
                if ((strcmp(start->command, command) == 0) && (strcmp(start->path1, path1) == 0))
                {
                    packet->port1 = start->port1;
                    strcpy(packet->ip1, start->ip1);
                    flag = 1;
                    break;
                }
            }
            start = start->next;
        }
        if (flag == 0)
        {
            return NULL;
        }
        else
        {
            return packet;
        }
    }
}