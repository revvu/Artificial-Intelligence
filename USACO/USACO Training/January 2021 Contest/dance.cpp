// USACO 2021 January Contest, Silver
// Problem 1. Dance Mooves
// Reevu Adakroy 1/25/2021

#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

#define MAX_N 100000

int N, K;

vector<pair<int, int>> adj[MAX_N];

int count_total;

void dfs(int pos, int i, int min){
    if(pos==i && min>=0) return;
    if(min<0) min =0;
    if(min+1>=K) min = min%K-1;
    vector<pair<int, int>> v = adj[pos];
    pair<int, int> q;
    q.first = min;
    q.second = -1;
    int index = upper_bound(v.begin(), v.end(), q) - v.begin();
    if(index == v.end()-v.begin()) index = 0; 
    cout << "\n" << index << "\n";
    count_total++;
    min = max(min, v[index].first);
    dfs(v[index].second, i, min+1);
}

int main(){
    cin >> N >> K;

    for(int i=0; i<K; i++){
        pair<int, int> p;
        cin >> p.first >> p.second;
        p.first--;
        p.second--;
        pair<int, int> q;
        q.first = i;
        q.second = p.second;
        adj[p.first].push_back(q);
        q.second = p.first;
        adj[p.second].push_back(q);
    }

    for(int i=0; i<N; i++){
        vector <pair<int, int>> v = adj[i];
        sort(v.begin(), v.end());
    }

    for(int i=0; i<N;i++){
        cout << i << ": ";
        for(auto pair : adj[i]){
            cout << "(" << pair.first << ", " << pair.second << "), ";
        }
        cout << "\n";
    }


    count_total = 0;
    dfs(3, 3, -1);
    cout << count_total << "\n";
    
    return 0;
}