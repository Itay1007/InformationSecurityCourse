#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int main()
{
    int x = 0x1111;
    int y = 0x2222;
    int sock = socket(2, 1, 0); // hardcoded socket(AF_INET, SOCK_STREAM, 0)
    struct sockaddr_in conn_addr = {0};
    conn_addr.sin_family = 2; // hardcoded AF_INET
    conn_addr.sin_addr.s_addr = 16777343; // hardcoded return value of inet_addr("127.0.0.1")
    conn_addr.sin_port = 14597; // hardcoded return value of htons(1337)
    connect(sock, (struct sockaddr *) &conn_addr, sizeof(conn_addr));
}
