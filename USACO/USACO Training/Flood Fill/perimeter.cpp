// USACO Silver 2019 January Icy Perimeter
// Reevu Adakroy 1/11/2021

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

int N;
#define MAXN 1000
char grid[MAXN][MAXN];
bool visited[MAXN][MAXN];
int area, perimeter_the_count;

void floodfill(int r, int c){
    
    if(visited[r][c]) return;
    if(grid[r][c]!='#') return;
    visited[r][c] = true;

    area++;
    // cout << "area increased \n";
    if(r==0) perimeter_the_count++;
    if(c==0) perimeter_the_count++;
    if(r==N-1) perimeter_the_count++;
    if(c==N-1) perimeter_the_count++;

    if(r-1 >= 0){
        if(grid[r-1][c]=='.') perimeter_the_count++;
        floodfill(r-1, c);
    }
    if(r+1 < N){
        if(grid[r+1][c]=='.') perimeter_the_count++;
        floodfill(r+1, c);
    }
    if(c-1 >= 0){
        if(grid[r][c-1]=='.') perimeter_the_count++;
        floodfill(r, c-1);
    }
    if(c+1 < N){
        if(grid[r][c+1]=='.') perimeter_the_count++;
        floodfill(r, c+1);
    }    
}

pair<int, int> solve(){
    // fill(comp.begin(), comp.end(), -1);
    
    int max_area=-1;
    int min_perimeter = 2147483647;
    
    for(int i=0; i<N; i++){
        for(int j =0; j<N; j++){
            if(visited[i][j]) continue;
            area = 0;
            perimeter_the_count = 0;
            floodfill(i, j);

            if(area==max_area){
                min_perimeter = min(min_perimeter, perimeter_the_count);
            }
            if(area>max_area){
                min_perimeter = perimeter_the_count;
                max_area = area;
            }
        } 
    }
    return {max_area, min_perimeter};
}

int main(){
    ifstream fin ("perimeter.in");
    fin >> N;

    for(int i = 0; i < N; i++){
        for(int j=0; j<N; j++){
            fin >> grid[i][j];
        }
    }

    auto p = solve();

    ofstream fout ("perimeter.out");

    fout << p.first << " " << p.second << "\n";
    return 0;
}