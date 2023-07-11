// USACO 2017 US Open Contest, Silver
// Problem 3. Where's Bessie?
//  Reevu Adakroy 1/22/2021

#include<iostream>
#include <fstream>
#include <vector>
#include <set>

#define MAX_N 20

using namespace std;

int N;
char grid[MAX_N][MAX_N];
int visited[MAX_N][MAX_N];

struct PCL {int minrow, maxrow, mincol, maxcol; };

vector<PCL> all;
vector<PCL> approved;

bool visitedPCL[MAX_N][MAX_N][MAX_N][MAX_N];

void floodfill(int r, int c, char a, int k, PCL p){
    if(r>=p.maxrow || c >= p.maxcol || r < p.minrow || c < p.mincol) return;
    if (visited[r][c] != -1) return;
    if (grid[r][c] != a) return;

    visited[r][c] == k;

    floodfill(r-1, c, a, k, p);
    floodfill(r+1, c, a, k, p);
    floodfill(r, c-1, a, k, p);
    floodfill(r, c+1, a, k, p);

}

void addPCL(int r1, int r2, int c1, int c2){

    PCL p;
    if (r1 == r2-1 && c1 == c2-1) return;
    if (visitedPCL[r1][r2][c1][c2]) return;
    p.minrow = r1;
    p.maxrow = r2;
    p.mincol = c1;
    p.maxcol = c2;
    visitedPCL[r1][r2][c1][c2] = true;
    all.push_back(p);

    addPCL(r1+1, r2, c1, c2);
    addPCL(r1, r2-1, c1, c2);
    addPCL(r1, r2, c1+1, c2);
    addPCL(r1, r2, c1, c2-1);
}

bool colorcheck(PCL p){
    set<char> colors;
    
    for(int i=p.minrow; i < p.maxrow; i++){
        for(int j=p.mincol; j<p.maxcol; j++){
            colors.insert(grid[i][j]);
        }
    }

    if (colors.size() > 2) return false;
    return floodcheck(p, colors);
}

bool floodcheck(PCL p, set<char> colors){
    bool singlecolor = false;
    bool multicolor = false;

    for (auto color: colors){
        int k = 0;
        for(int i=p.minrow; i<p.maxrow; i++){
            for(int j=p.mincol; j<p.maxcol; j++){
                if (visited[i][j]) continue;
                visited[i][j] = true;
                floodfill(i, j, color, k++, p);
            }
        }
    }
    
}

bool bigcheck(PCL p){
    for(auto rect : approved){
        if(rect.minrow<=p.minrow && rect.maxrow>=p.maxrow && rect.mincol<=p.mincol && rect.maxcol>=p.maxcol) return false;
    }
    return true;
}

int main(){

    ifstream fin ("where.in");

    fin >> N;
    for(int i =0; i < N; i++){
        for(int j=0; j <N; j++){
            fin >> grid[i][j];
        }
    }

    addPCL(0, N, 0, N);
    for(auto rect : all){
        if(colorcheck(rect) && bigcheck(rect)){
            approved.push_back(rect);
        }
    }

    ofstream fout ("where.out");

    return 0;
}