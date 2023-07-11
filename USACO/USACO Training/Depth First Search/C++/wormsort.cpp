// USACO 2020 January Problem 3 Wormsort
// Reevu Adakroy 1/10/2021

// use dfs to determine if every value is in the same component as its cow number
// binary search on the answer

#include <iostream>
#include <fstream>
#include <vector>
#include <set>
#include <algorithm>

using namespace std;

const int MX = 1e5;

vector<pair<int, int>> g[MX];
vector<int> ar(MX), component(MX);
int n, m;

void dfs(int v, int label, int minW){
    component[v] = label;

    for(auto x: g[v]){
        if (x.second < minW || component[x.first] != -1) continue;
        dfs(x.first, label, minW);
    }
}

bool ok(int minW){
    fill (component.begin(), component.end(), -1);

    int label = 0;
    for(int i=0; i<n; i++){
        if(component[i]!=-1) continue;
        dfs(i, label++, minW);
    }

    for(int i=0; i<n; i++){
        if(component[i]!=component[ar[i]]) return false;
    }
    return true;
}

int main(){
    ifstream fin ("wormsort.in");
    fin >> n >> m;
    for(int i=0; i<n; i++){
        int a;
        fin >> a;
        ar[i]=a-1;
    }

    for(int i=0; i<m; i++){
        int a, b, w;
        fin >> a >> b >> w;
        g[a-1].push_back({b-1, w});
        g[b-1].push_back({a-1, w});
    }

    int sol = -1;
    int lo = 1, hi = 1e9+1;
    int top = hi;
    while(lo<=hi){
        int mid = lo + (hi-lo)/2;

        if(ok(mid)){
            sol = max(sol, mid);
            lo = mid+1;
        } else {
            hi = mid-1;
        }
    }

    ofstream fout ("wormsort.out");
    fout << (sol == top ? -1 : sol) << "\n";

}
