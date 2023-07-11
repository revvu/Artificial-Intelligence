// USACO 2020 US Open Contest, Silver
// Problem 1. Social Distancing
// Reevu Adakroy 1/23/2021

#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

using namespace std;

vector<pair<int, int>> fields;
int N, M;


bool works(int D){
    int index = 0;
    int point = fields[index].first;
    for(int i=0; i<N-1; i++){
        // place one cow

        // shift to new point
        point = point + D;
        // if its in the same region, do nothing
        if (point > fields[index].second){
            while(index < M && point > fields[index].second)
                index++;
            
            if(index >= M) return false;

            if (point < fields[index].first)
                point = fields[index].first;
        }

    }

    return true;
}

bool compare(pair<int, int> a, pair<int, int> b){
    return a.first < b.first;
}

int main(){

    ifstream fin ("socdist.in");
    fin >> N >> M;

    for(int i=0; i <M; i++){
        pair<int, int> p;
        fin >> p.first >> p.second;
        fields.push_back(p);
    }
    

    sort(fields.begin(), fields.end(), compare);

    int max_val = fields.back().second;
    int lo = 0; 
    int hi = max_val / N + 1;

    int sol = -1; 
    while(lo <= hi){
        int mid = (lo+hi+1)/2;

        if(works(mid)){
            lo = mid+1;
            sol = max(sol, mid);
        }

        else{
            hi = mid-1;
        }
    } 

    ofstream fout ("socdist.out");
    fout << sol;
    return 0;
}