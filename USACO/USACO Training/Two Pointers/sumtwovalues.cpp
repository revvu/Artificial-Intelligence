// CSES Problem Set
// Sum of Two Values
// Reevu Adakroy 4/7/2021

#include<iostream>
#include<algorithm>
#include<vector>

using namespace std;

int n, x;
vector<int> arr;
vector<int> id;

bool cmp(int a, int b){return arr[a]<arr[b];}

int main(){
    cin >> n >> x;
    int a;
    for(int i=0;i<n;i++){
        cin >> a;
        arr.push_back(a);
    }
    
    for(int i=0; i<n;i++){
        id.push_back(i);
    }
 
    sort(begin(id), end(id), cmp);

    // for(int i=0; i<n;i++){
    //     cout << " " << id[i];
    // }
    // cout << "\n";

    int left = 0;
    int right = n-1;

    bool found = false;
    int sum;
    while(left!=right){
        sum = arr[id[left]]+arr[id[right]];
        if (sum == x){ 
            cout << id[left]+1 << " " << id[right]+1 << "\n";
            found = true;
            break;   
        }
        else if(sum>x){ right+=-1; }
        else { left+=1; }
    }

    if(!found){ cout << "IMPOSSIBLE" << "\n"; }

    return 0;
}