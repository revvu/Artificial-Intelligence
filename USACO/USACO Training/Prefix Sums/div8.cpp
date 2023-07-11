// USACO 2016 January Contest, Silver
// Problem 2. Subsequences Summing to Sevens
// Reevu Adakroy 1/23/2021

#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

using namespace std;

int main(){

    int N;
    ifstream fin ("div7.in");
    fin >> N;
    
    vector<int > arr;

    for(int i =0; i < N; i++){
        int a;
        fin >> a;
        arr.push_back(a);
    }    

    vector <int> prefix;
    prefix.push_back(0);
    for(int i=0; i<N; i++){
        prefix.push_back((prefix.back()+arr[i])%7);
    }

    int max_dist = find(prefix.begin(), prefix.end(), 0) - prefix.begin();

    for(int i=0; i<7; i++){
        
        int min_index = -1;
        int max_index = -1;

        for(int j=0; j<N+1; j++){
            if(prefix[j] == i){
                if(min_index == -1) min_index = j;
                else{
                    max_index = j;
                }
            }
        }
        max_dist = max(max_index-min_index, max_dist);
    } 
    ofstream fout ("div7.out");
    fout << max_dist << endl;
    return 0;
}