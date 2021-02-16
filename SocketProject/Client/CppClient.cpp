#include <iostream>
#include <string>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <fstream>
#include <vector>
#include <filesystem>
using namespace std;
namespace fs = std::__fs::filesystem;

//Socket Class
class Socket {
private:
    struct sockaddr_in addr;
    
public:
    int sock;
    
    Socket(unsigned int ip,int port){
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

//string char convert
char* convChar(string str){
    vector<char> vc(str.begin(), str.end());
    vc.push_back('\0');
    char* c = &*vc.begin();
    return c;
}

string convStr(char* c){
    string str(c);
    return str;
}

//Functions
void fileList(fs::path storage){
    fs::directory_iterator itr(storage);
    while (itr != fs::end(itr)){
        const fs::directory_entry& entry = *itr;
        string ext = entry.path().extension();
        if (ext==".txt" or ext==".png" or ext==".jpg"){
            cout << entry.path() << endl;
        }
        itr++;
    }
}

void sendTxt(Socket server, fs::path storage, string fn){
    ifstream ReadFile;
    ReadFile.open(storage.string() + fn);
    
    if (ReadFile.is_open()){
        string tmp;
        getline(ReadFile,tmp);
        char* msg = convChar(tmp);
        
        write(server.sock,msg,sizeof(tmp));
    }
}

void readMsg(Socket server){
    char message[1024] = {};
    read(server.sock,message,sizeof(message));
    cout << message << endl;
}

//Main Function
int main(int argc, const char * argv[]) {
    fs::path storage("/Users/evan/Downloads/");
    
    unsigned int ip = inet_addr("203.227.140.199");
    Socket server = Socket(ip, 9966);
    
    cout << "Server File List : " << endl;
    readMsg(server);
    cout << "\n Storage File List : " << endl;
    fileList(storage);
    cout << "----------" << endl;
    
    close(server.sock);
    return 0;
}
