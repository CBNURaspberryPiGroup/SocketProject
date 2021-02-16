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

int sendTxt(Socket server, fs::path storage, string fn){
    ifstream ReadFile;
    ReadFile.open(storage.string() + fn);
    int trSize = 0;
    
    if (ReadFile.is_open()){
        while(!ReadFile.eof()){
            string tmp;
            getline(ReadFile,tmp);
            char* msg = convChar(tmp);
            
            write(server.sock,msg,sizeof(tmp));
            trSize += sizeof(tmp);
        }
        ReadFile.close();
    }
    return trSize;
}

int recvTxt(Socket server, fs::path storage, string fn){
    ofstream WriteFile;
    WriteFile.open(storage.string()+fn);
    int trSize = 0;
    
    if (WriteFile.is_open()){
        char msg[] = {};
        recv(server.sock,msg,strlen(convChar(fn))+20,0);
        cout << msg << endl;
        while (true){
            char msg[1024] = {};
            ssize_t recvLen = recv(server.sock,msg,1024,0);
            cout << msg << recvLen << endl;
            if (recvLen > 0){
                WriteFile.write(msg, strlen(msg));
            }
            else {break;}
        }
    }
    WriteFile.close();
    return trSize;
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
    
    while (true){
        cout << ">> ";
        string cmd;
        getline(cin,cmd);
        cout << convChar(cmd) << endl;
        
        char* ex = strtok(convChar(cmd)," ");
        cout << ex << endl;
        if (strcmp(ex,"push")==0){
            break;
        }
        else if(strcmp(ex,"pull")==0){
            send(server.sock,convChar(cmd),strlen(convChar(cmd)),0);
            cout << recvTxt(server, storage, strtok(NULL," ")) << "Transmitted" << endl;
        }
        else if(strcmp(ex,"exit")==0){
            break;
        }
    }
    
    close(server.sock);
    return 0;
}
