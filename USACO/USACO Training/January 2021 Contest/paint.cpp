// USACO 2021 January Contest, Silver
// Problem 2. No Time to Paint
// Reevu Adakroy 1/25/2021

#include <iostream>
#include <vector>
#include <set>

using namespace std;

int main(){

    int n, q;
    cin >> n >> q;

    vector<int> v;
    vector<pair<int,int>> qs; 
    for(int i=0; i<n; i++){
        char a;
        cin >> a;
        v.push_back(a-65);
    }

    for(int i=0; i<q; i++){
        pair<int, int> a;
        cin >> a.first >> a.second;
        qs.push_back(a);
    }

    vector<int> prefix;
    vector<int> color;
    set<int> colors;
    colors.insert(v[0]);
    prefix.push_back(0);
    prefix.push_back(0);
    color.push_back(0);
    color.push_back(0);
    bool down = false;
    int cur = v[0];
    for(int i=1; i<n; i++){
        int a = prefix.back();
        if(v[i]<cur) down=true;
        if(v[i]>cur && down) {
            a++;
            down = false;
        }
        cur = v[i];
        prefix.push_back(a);

        int b = color.back();
        if(!colors.count(v[i])) b++;
        colors.insert(v[i]);
        color.push_back(b);
    }

    // for(int i=0; i<n; i++){
    //     cout << prefix[i] << " ";
    // }

    // cout << "\n";

    // for(int i=0; i<n+1; i++){
    //     cout << color[i] << " ";
    // }

    // cout << "\n";

    for(int i=0; i<q; i++){
        pair<int, int> b = qs[i];
        int total = color[b.first-1]+color[n]-color[b.second]+2-(b.first==1 || b.second == n);
        // cout << "color: " << total << "\n";
        total += prefix[b.first-1]+prefix[n]-prefix[b.second];
        // cout << "new total: " <<  total << "\n";
        cout << total << "\n";
    }

    return 0;
}