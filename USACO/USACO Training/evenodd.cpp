// USACO 2021 January Contest, Bronze
// Problem 2. Even More Odd Photos
// Reevu Adakroy 3/29/2021

#include <iostream>
#include <algorithm>

using namespace std;

int N;
int evens=0;
int odds=0;
int main() {
    
    cin >> N;
    int a;
    for(int i; i<N; i++){
        cin >> a;
        if(a%2) odds++;
        else{ evens++; }
    }

    if(evens>odds){
        cout << odds*2+1 << "\n";
    } 
    else if(evens==odds) {
        cout << odds*2 << "\n";
    }
    else {
        odds += -evens;
        cout << 2*evens + odds/3*2 + int(odds%3==2) - int(odds%3==1) << "\n";
    }
}