#include <iostream>
#include <vector>
#include <algorithm>
#include <fstream>

using namespace std;
#define MAX_N 100000

vector<pair<int, int>> C;
vector<int> nbrs[MAX_N];

int visited[MAX_N];

struct border {int x1, x2, y1, y2; };

void dfs(int v, int k, border &bb){
    visited[v] = k;
    bb.x1 = min(bb.x1, C[v].first);
    bb.x2 = max(bb.x2, C[v].first);
    bb.y1 = min(bb.y1, C[v].second);
    bb.y2 = max(bb.y2, C[v].second);

    for(int x: nbrs[v]){
        if(visited[x]!=0) continue;
        dfs(x, k, bb);
    }
}

int main() {
    ifstream fin ("fenceplan.in");
    // freopen("fenceplan.in", "r", stdin);
    // freopen("fenceplan.out", "w", stdout);

    int N, M;
    fin >> N >> M;

    for(int i=0; i<N; i++)
    {
        int x, y;
        fin >> x >> y;
        C.push_back({x,y});
    }

    for(int i=0; i<M; i++){
        int a,b;
        fin >> a >> b;
        nbrs[a-1].push_back(b-1);
        nbrs[b-1].push_back(a-1);
    }

    int perimeter = 2147483647;
    int k = 0;
    for(int cow = 0; cow < N; cow++){
        if(visited[cow]!=0) continue;
        border bb = {2147483647, 0, 2147483647, 0};
        dfs(cow, ++k, bb);

        perimeter = min(perimeter, 2*(bb.x2-bb.x1+bb.y2-bb.y1));
    }
    ofstream fout ("fenceplan.out");
    fout << perimeter;

    return 0;
}