// USACO 2019 January Contest, Silver
// Problem 3. Mountain View
// Reevu Adakroy 1/18/2021

#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

using namespace std;

#define MAX_N 100000

int cid[MAX_N];
int neg[MAX_N];
int pos[MAX_N];
int x[MAX_N];
int y[MAX_N];
int n;


bool compare(int a, int b){
    if(neg[a]==neg[b]){
        return pos[a] > pos[b];
    }
    return neg[a] < neg[b];
}

int main(){
    
    ifstream fin ("mountains.in");

    fin >> n;
    for(int i =0; i < n; i++){
        fin >> x[i] >> y[i];
        pos[i]=x[i]+y[i];
        neg[i]=x[i]-y[i];
        cid[i]=i;
    }
    sort(cid, cid+n, compare);
    int max_pos = -1;
    int ans = 0;
    for(int i =0; i < n; i++){
        if(pos[cid[i]] > max_pos){
            ans++;
            max_pos = pos[cid[i]];
        }
    }

    // cout << "x: ";
    // for(int i =0; i < n; i++){
    //     cout << x[i] << " ";
    // }
    // cout << "\n";
    // cout << "y: ";
    // for(int i =0; i < n; i++){
    //     cout << y[i] << " ";
    // }
    // cout << "\n";
    // cout << "neg: ";
    // for(int i =0; i < n; i++){
    //     cout << neg[i] << " ";
    // }
    // cout << "\n";
    // cout << "pos: ";
    // for(int i =0; i < n; i++){
    //     cout << pos[i] << " ";
    // }
    // cout << "\n";
    // cout << "cid: ";
    // for(int i =0; i < n; i++){
    //     cout << cid[i] << " ";
    // }

    ofstream fout ("mountains.out");
    fout << ans << "\n";
    return 0;
}