//
//  main.cpp
//  RPG_Socket
//
//  Created by 이정호 on 2021/01/14.
//

#include <iostream>
#include <string>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

int main(int argc, const char * argv[]) {
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = inet_addr("203.227.140.199");
    addr.sin_port = htons(9966);
    
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (connect(sock, (struct sockaddr*)&addr, sizeof(addr)) == -1){
        std::cout << "Connection Error" << std::endl;
    }
    
    char msg[] = "Hello world\n";
    write(sock,msg,sizeof(msg));
    
    char message[1024] = {0x00,};
    read(sock,message,sizeof(message)-1);
    std::cout << message << std::endl;
    
    close(sock);
    return 0;
}
