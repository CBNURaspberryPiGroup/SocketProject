#include <iostream>
#include <string>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <fstream>
#include <vector>
using namespace std;

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
            cout << "Connection Error" << endl;
        }
    }
};

char* convChar(string str){
    vector<char> vc(str.begin(), str.end());
    vc.push_back('\0');
    char* c = &*vc.begin();
    return c;
}

int main(int argc, const char * argv[]) {
    unsigned long int ip = inet_addr("203.227.140.199");
    Socket server = Socket(ip, 9966);
    
    /*
    char msg[] = "Hello world\n";
    write(server.sock,msg,sizeof(msg));
     */
    
    ifstream ReadFile;
    ReadFile.open("/Users/evan/Documents/PyVacation/Ref/IdealGasPV.txt");
    
    if (ReadFile.is_open()){
        string tmp;
        getline(ReadFile,tmp);
        char* msg = convChar(tmp);
        
        write(server.sock,msg,sizeof(tmp));
    }
    
    char message[1024] = {0x00,};
    read(server.sock,message,sizeof(message)-1);
    cout << message << endl;
    
    close(server.sock);
    return 0;
}
