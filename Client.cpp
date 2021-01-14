#include <iostream>
#include <string>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

class Socket {
private:
    struct sockaddr_in addr;
    
public:
    int sock;
    
    Socket(unsigned long int ip,int port){
        memset(&addr, 0, sizeof(addr));
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = ip;
        addr.sin_port = htons(port);
        
        sock = socket(AF_INET, SOCK_STREAM, 0);
        if (connect(sock, (struct sockaddr*)&addr, sizeof(addr)) == -1){
            std::cout << "Connection Error" << std::endl;
        }
    }
};

int main(int argc, const char * argv[]) {
    unsigned long int ip = inet_addr("203.227.140.199");
    Socket server = Socket(ip, 9966);
    
    char msg[] = "Hello world\n";
    write(server.sock,msg,sizeof(msg));
    
    char message[1024] = {0x00,};
    read(server.sock,message,sizeof(message)-1);
    std::cout << message << std::endl;
    
    close(server.sock);
    return 0;
}
