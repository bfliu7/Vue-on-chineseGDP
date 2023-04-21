#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#define SERVER_PORT 2020
#define SERVER_IP  "127.0.0.1"
int main(int argc, char *argv[]){
    int sockfd;
    char *message;
    struct sockaddr_in servaddr;
    int n;
    char buf[64];
    message = argv[1];
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    memset(&servaddr, '\0', sizeof(struct sockaddr_in));
    servaddr.sin_family = AF_INET;
    inet_pton(AF_INET, SERVER_IP, &servaddr.sin_addr);
    servaddr.sin_port = htons(SERVER_PORT);
    connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr));
    write(sockfd, message, strlen(message));
    n = read(sockfd, buf, sizeof(buf)-1);
    printf("message from server: %s\n", buf);
    printf("OVER.\n");
    close(sockfd);
    return 0;
}