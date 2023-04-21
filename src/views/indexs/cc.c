#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <ctype.h>
#define SERVER_PORT 2020
int main()
{
	int sock = socket(AF_INET,SOCK_STREAM,0);
	struct sockaddr_in server_addr;
	memset(&server_addr,0,sizeof(server_addr));
	server_addr.sin_family = AF_INET;	//指定协议族
	server_addr.sin_addr.s_addr = htonl(INADDR_ANY);//监听本地所有ip
	server_addr.sin_port = htons(SERVER_PORT);//绑定端口号
	bind(sock,(struct sockaddr*)&server_addr,sizeof(server_addr));
	listen(sock,128);
	printf("waiting:\n");
	while(1)
	{
		struct sockaddr_in client;
		int client_sock;
		socklen_t client_len = sizeof(client);
		char client_ip[33];
		client_sock = accept(sock,(struct sockaddr*)&client,&client_len);
		char buf[256];
		int len = read(client_sock,buf,sizeof(buf) - 1);
		buf[len] = 0;
		printf("message from client: %s\n",buf);	
		len =  write(client_sock,buf,len);	
		close(client_sock);
	}
    return 0;
}