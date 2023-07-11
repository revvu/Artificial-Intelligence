// USACO 2020 December Contest, Silver
// Problem 2. Rectangular Pasture
// Reevu Adakroy 1/24/2021

#include <iostream>
#include <algorithm>


using namespace std;

#define MAX_N 2500

int Psum[MAX_N+1][MAX_N+1];
int N;
pair<int, int> P[MAX_N];

void printPsum(){
    for(int i=0; i<N+1; i++){
        for(int j=0; j<N+1; j++){
            cout << Psum[i][j] << " ";
        }
        cout << "\n";
    }
}

bool compY(pair<int, int> a, pair<int, int> b){
    return a.second < b.second;
}

int parseSum(int x1, int x2, int y1, int y2){
    return Psum[x2+1][y2+1] - Psum[x1][y2+1] - Psum[x2+1][y1] + Psum[x1][y1];
}

int main(){

    cin >> N;
    for(int i=0; i<N; i++){
        pair<int, int> point;
        cin >> point.first >> point.second;
        P[i]=point; 
    }
    
    sort(P, P+N);
    for(int i=0; i<N; i++){
        P[i].first = i+1;
    }
    sort(P, P+N, compY);
    for(int i=0; i<N; i++){
        P[i].second = i+1;
    }

    for(int i=0; i<N; i++){
        Psum[P[i].first][P[i].second] = 1;
    }
    // cout << "\n";
    // printPsum();
    // cout << "\n";

    // prefix sum

    for(int i=1; i<N+1; i++){
        for(int j=1; j<N+1; j++){
            Psum[i][j] += Psum[i-1][j] + Psum[i][j-1] - Psum[i-1][j-1];
        }
    }
    
    // printPsum();
    long long sol = 0;
    for(int i=0; i<N; i++){
        for(int j=i; j<N; j++){
            int x1 = min(P[i].first, P[j].first);
            int x2 = max(P[i].first, P[j].first);

            sol+= parseSum(0, x1-1, i, j) * parseSum(x2-1, N-1, i, j);
        }
    }

    // count empty
    cout << sol+1; 

    // cout << parseSum(0, 3, 0, 3) << endl;

    return 0;
}