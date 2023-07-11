// USACO 2017 February Contest, Silver
// Problem 3. Why Did the Cow Cross the Road III
// Reevu Adakroy 1/22/2021

#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>
#include <set>
#include <tuple>


using namespace std;

int N, K, R;
bool vis[100][100];
set<tuple<int, int, int, int>> roads;

int di[4] = {1, -1, 0, 0}, dj[4] = {0, 0, 1, -1};

vector<pair<int, int>> cows;

void printVis(){
    for(int a = 0; a<N; a++){
        for(int b=0; b<N; b++){
            cout << vis[a][b] << " ";
        }
        cout << "\n";
    }
}

void ff(int i, int j, int i1, int j1){
    if( i < 0 || j < 0 || i >= N || j >= N || roads.count(tie(i, j, i1, j1))) return;

    if(vis[i][j]) return;

    vis[i][j] = true;

    for(int k=0; k<4; k++){
        ff(i+di[k], j+dj[k], i, j);
    }
}

int main(){

    ifstream fin ("countcross.in");

    fin >> N >> K >> R;

    for(int i=0; i<R; i++){
        pair<int, int> r1, r2;
        fin >> r1.first >> r1.second >> r2.first >> r2.second;
        r1.first--;
        r1.second--;
        r2.first--;
        r2.second--;
        roads.insert(tie(r1.first, r1.second, r2.first, r2.second));
        roads.insert(tie(r2.first, r2.second, r1.first, r1.second));
    }

    for(int i=0; i < K; i++){
        pair<int, int> cow;
        fin >> cow.first >> cow.second; 
        cow.first--;
        cow.second--;
        cows.push_back(cow);
    }

    int sol = 0;

    for(int i =0; i < K; i++){

        ff(cows[i].first, cows[i].second, -1, -1);

        for(int j=i+1; j<K; j++){
            if(vis[cows[j].first][cows[j].second] != true) {
                sol++; 
            }
        }

        for(int a =0; a < N; a++){
            for(int b=0; b<N; b++){
                vis[a][b] = false;
            }
        }
    }

    ofstream fout ("countcross.out");
    fout << sol;

    return 0;
}