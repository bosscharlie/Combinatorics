#include<iostream>
#include<vector>
using namespace std;
int total_count = 0;
int num_count = 0;

bool illegal(int x1,int y1,int x2,int y2,vector<vector<bool> > key_status){//通过枚举不合法情况，判断本次连接是否合法
    int num1 = x1*3+y1+1;
    int num2 = x2*3+y2+1;
    int a = num1<num2? num1 : num2;
    int b = num1<num2? num2 : num1;
    if(key_status[0][1]==false && a==1&&b==3){
        return true;
    }else if(key_status[1][0]==false && a==1&&b==7){
        return true;
    }else if(key_status[1][1]==false && ((a==1&&b==9)||(a==2&&b==8)||(a==3&&b==7)||(a==4&&b==6))){
        return true;
    }else if(key_status[1][2]==false && a==3&&b==9){
        return true;
    }else if(key_status[2][1]==false&& a==7&&b==9){
        return true;
    }else{
        return false;
    }
}

void dfs(vector<vector<bool> > key_status,int x,int y,int count){//深度优先搜索
    if(count == 1){
        num_count++;
        return;
    }
    for(int i=0;i<3;i++){
        for(int j=0;j<3;j++){
            if(!key_status[i][j]){//如果当前点还未被访问过
                int distance = (x-i)*(x-i)+(y-j)*(y-j);
                if(!illegal(x,y,i,j,key_status)){
                    vector<vector<bool> > temp = key_status;
                    temp[i][j]=true;
                    dfs(temp,i,j,count-1);
                }
            }
        }
    }
}

int main(){
    for(int n=4;n<=9;n++){
        num_count = 0;
        for(int i=0;i<3;i++){
            for(int j=0;j<3;j++){
                vector<vector<bool> > keyboard(3,vector<bool>(3));
                keyboard[i][j]=true;
                dfs(keyboard,i,j,n);
            }
        }
        cout<<n<<" nodes:"<<num_count<<endl;
        total_count+=num_count;
    }
    cout<<"total_num: "<<total_count<<endl;
    return 0;
}