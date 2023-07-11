// USACO 2020 December Contest, Silver
// Problem 3. Stuck in a Rut
// Reevu Adakroy 1/24/2021

#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int N;
vector<int> eastX;
vector<int> eastY;
vector<int> northX;
vector<int> northY;
vector<int> allX;
vector<int> allY;
vector<int> eastID;
vector<int> northID;
vector<int> cid;
vector<int> northBlock;
vector<int> eastBlock;
bool stopped[1000];


bool compareEast(int a, int b){
    if(eastX[a] == eastX[b]){
        return eastY[a] < eastY[b];
    }
    return eastX[a] < eastX[b];
}

bool compareNorth(int a, int b){
    if(northY[a] == northY[b]){
        return northX[a] < northX[b];
    }
    return northY[a] < northY[b];
}

bool compareLeastXLeastYNorth(int a, int b){
    if(northX[a]==northX[b])
        return northY[a] < northY[b];
    return northX[a] < northX[b];
}

bool compareLeastXLeastYEast(int a, int b){
    if(eastX[a]==eastX[b])
        return eastY[a] < eastY[b];
    return eastX[a] < eastX[b];
}

int main(){

    cin >> N;

    int eastCount = 0;
    int northCount = 0;

    for(int i=0; i<N; i++){
        char a;
        int x, y;
        cin >> a >> x >> y;
        if(a=='E'){
            eastX.push_back(x);
            eastY.push_back(y);
            eastID.push_back(i);
            eastBlock.push_back(i);
            eastCount++;
        }
        else{
            northX.push_back(x);
            northY.push_back(y);
            northID.push_back(i);
            northBlock.push_back(i);
            northCount++;
        }
        allX.push_back(x);
        allY.push_back(y);
        cid.push_back(0);
    }

    sort(northID.begin(), northID.end(), compareNorth);
    sort(eastID.begin(), eastID.end(), compareEast);
    sort(northBlock.begin(), northBlock.end(), compareLeastXLeastYNorth);
    sort(eastBlock.begin(), eastBlock.end(), compareLeastXLeastYEast);

    int eastIndex = 0;
    int northIndex = 0;

    while(northIndex < northCount && eastIndex < eastCount){
        int min_east = eastID[eastIndex];
        int min_north = northID[northIndex];

        if(allX[min_north]-allX[min_east] > (allY[min_east] - allY[min_north])){
            cid[min_north]++;
            eastIndex++;
        }
        else if(allX[min_north]-allX[min_east] < (allY[min_east] - allY[min_north])){
            cid[min_east]++;
            northIndex++;
        }
        else{
            northIndex++;
            eastIndex++;
            cid[northID[northIndex]]++;
            cid[eastID[eastIndex]]++;
        }
    }

    for(int i=0; i<N; i++){
        cout << cid[i] << "\n";
    }

    return 0;
}