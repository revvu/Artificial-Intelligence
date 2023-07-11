// USACO 2020 December Contest, Silver
// Problem 1. Cowntagion
// Reevu Adakroy 1/23/2021

#include <iostream>
#include <vector>
#include <cmath>
#include <math.h> 

using namespace std;

#define MAX_N 100000

int n;
bool visited[MAX_N];

vector<int> farms[MAX_N];
int days;


void dfs(int farm){

    if(visited[farm]) return;

    visited[farm] = true;

    int cow_count = 1;
    int unvisited_count = 1;
    for(int subfarm : farms[farm]){
        if(visited[subfarm] == false) {
            unvisited_count += 1;
            dfs(subfarm);
        }
    }

    int result = ceil(log2(unvisited_count));
    days+=result;
    days+=unvisited_count-1;


}

int main(){

    cin >> n;

    for(int i=0; i<n-1;i++){
        int farm1, farm2;
        cin >> farm1 >> farm2;
        farms[farm1-1].push_back(farm2-1);
        farms[farm2-1].push_back(farm1-1);
    }

    dfs(0);

    cout << days;

    return 0;
}