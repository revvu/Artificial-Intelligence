// USACO 2016 US Open Contest, Silver
// Problem 2. Diamond Collector
//  Reevu Adakroy 1/24/2021

#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

using namespace std;

int N, K;
vector<int> diamonds;

int main(){

    ifstream fin ("diamond.in");

    fin >> N >> K;
    for(int i = 0; i<N; i++){
        int size;
        fin >> size;
        diamonds.push_back(size);
    }

    sort(diamonds.begin(), diamonds.end());

    int top_count = 0;
    int second_count = 0;

    int index1 = 0;
    int index2 = 1;

    int count = 0;

    while(index2 < N){
        if(diamonds[index2]-diamonds[index1] <= K)
            index2++;
            count++;
        
        
    }

    ofstream fout ("diamond.out");

    return 0;
}