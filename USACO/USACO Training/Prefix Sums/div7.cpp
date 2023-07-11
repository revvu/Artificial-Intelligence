// USACO 2016 January Silver Summing to Sevens
// Reevu Adakroy 1/17/2021

#include<iostream>
#include<fstream>
#include<vector>
#include <algorithm>

using namespace std;

int N;
#define MAX_N 50000
vector<int> arr(MAX_N);
vector<int> prefix(MAX_N);

void prefix_sum(){
    prefix[0] = 0;
    for(auto i: arr){
        prefix[i] = (arr[i]+prefix[i-1])%7;
    }
}

int main(){

    ifstream fin ("div7.in");

    fin >> N;

    for(int i=0; i < N; i++){
        int a;
        fin >> a;
        arr[i] = a;
        arr[i]=arr[i]%7;
    }


    prefix_sum();

    int max_difference = 0;
    
    for(int i =0; i<7; i++){
        auto start_index = find(prefix.begin(), prefix.end(), i);
        if (start_index == prefix.end()) continue;

        auto end_index = find(prefix.end(), prefix.begin(), i);

        int difference = end_index - start_index;

        max_difference = max(max_difference, difference);
    }

    ofstream fout("div7.out");
    fout << max_difference;
    cout << max_difference;

    return 0;
}