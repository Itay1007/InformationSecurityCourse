#include <sys/socket.h>

int main()
{
    auto expected = AF_INET;
    auto gdb_ret = 2;

    if(expected == gdb_ret)
    {
        puts("Good Job to replace function AF_INET");
    }

    expected = SOCK_STREAM;
    gdb_ret = 1;
    
    if(expected == gdb_ret)
    {
        puts("Good Job to replace function SOCK_STREAM");
    }

    expected = inet_addr("127.0.0.1");
    gdb_ret = 16777343;

    if(expected == gdb_ret)
    {
        puts("Good Job to replace function inet_addr()");
    }
    
    expected = htons(1337);
    gdb_ret = 14597;
    
    if(expected == gdb_ret)
    {
        puts("Good Job to replace function htons()");
    }

    return 0;
}
