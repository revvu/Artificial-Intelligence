// USACO 2019 February Contest, Gold
// Problem 3. Painting the Barn
// Reevu Adakroy 1/24/2021

#include <iostream>
#include <fstream>
#include <algorithm>

using namespace std;

#define MAX_N 100000

int N, K;
int Psum[201][201];

int max_dimension;

void printPsum(){
    for(int i=0; i<max_dimension; i++){
        for(int j=0; j<max_dimension; j++){
            if(Psum[i][j] < 0 || Psum[i][j] >= 10){
                cout << " " << Psum[i][j];
            }
            else{
                cout << "  " << Psum[i][j];
            }
        }
        cout << "\n";
    }
}

int main(){
    
    cin >> N >> K;

    max_dimension = 0;
    for(int i=0; i<N; i++){
        pair<int, int> corner1, corner2;
        cin >> corner1.first >> corner1.second >> corner2.first >> corner2.second;
        Psum[corner1.first+1][corner1.second+1] += 1;
        Psum[corner2.first+1][corner2.second+1] += 0;
        Psum[corner1.first+1][corner2.second+1] += -1;
        Psum[corner2.first+1][corner1.second+1] += -1;
        max_dimension = max(max_dimension, corner1.second+1);
        max_dimension = max(max_dimension, corner2.second+1);
    }
    max_dimension+=2;
    printPsum();
    cout << "\n";

    for(int i=1; i<max_dimension; i++){
        for(int j=1; j<max_dimension; j++){
            Psum[i][j] += Psum[i-1][j] + Psum[i][j-1] - Psum[i-1][j-1];
        }
    }

    for(int i=1; i<max_dimension; i++){
        for(int j=1; j<max_dimension; j++){
            if(Psum[i][j]==K) Psum[i][j]= -1;
            else if(Psum[i][j]==(K-1)) Psum[i][j] = 1;
            else Psum[i][j] = 0;
        }
    }

    printPsum();
    cout << "\n";
    for(int i=1; i<max_dimension; i++){
        for(int j=1; j<max_dimension; j++){
            Psum[i][j] += Psum[i-1][j] + Psum[i][j-1] - Psum[i-1][j-1];
        }
    }

    printPsum();

    int count = 0;
    for(int i=0; i<max_dimension; i++){
        for(int j=0; j<max_dimension; j++){
            if(Psum[i][j] == -1) count++;
        }
    }
    cout << count;
    return 0;
}