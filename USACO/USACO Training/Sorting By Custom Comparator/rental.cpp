// USACO 2018 January Contest, Silver
// Problem 2. Rental Service
// Reevu Adakroy 1/17/2021

#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>


using namespace std;

int N, M, R;
vector<long long> cows;
struct store {long long count, cost; };
vector<store> stores;
vector<long long> renters;
vector<long long> renters_prefix;
vector<long long> cows_prefix;
vector<long long> store_prefix;
vector<long long> store_value_prefix;


bool compare_store(store a, store b){
    return a.cost > b.cost;
}

bool compare_cows(long long a, long long b){
    return b>a;
}

bool compare_renters(long long a, long long b){
    return a>b;
}

int main(){

    ifstream fin ("rental.in");
    fin >> N >> M >> R;
    
    for(int i =0; i < N; i++){
        long long a;
        fin >> a;
        cows.push_back(a);
    }

    for(int i= 0; i< M; i++){
        long long count, cost;
        store s;
        fin >> s.count >> s.cost;
        stores.push_back(s);
    }

    for(int i=0; i < R; i++){
        long long a;
        fin >> a;
        renters.push_back(a);
    }

    sort(cows.begin(), cows.end(), compare_cows);
    sort(renters.begin(), renters.end(), compare_renters);
    sort(stores.begin(), stores.end(), compare_store);

    // prefixed sum on renters
    renters_prefix.push_back(0);
    for(int i=0; i<R; i++){
        renters_prefix.push_back(renters[i]+renters_prefix.back());
    }

    
    store_prefix.push_back(0);
    for(int i=0; i<M; i++){
        store_prefix.push_back(stores[i].count+store_prefix.back());
    }

    store_value_prefix.push_back(0);
    for(int i=0; i<M; i++){
        store_value_prefix.push_back(stores[i].count*stores[i].cost+store_value_prefix.back());
    }

    int total_cow = 0;
    for(auto cow: cows){
        total_cow+=cow;
    }

    // prefixed sum on cows
    cows_prefix.push_back(total_cow);
    for(int i=0; i<N; i++){
        cows_prefix.push_back(cows_prefix.back()-cows[i]);
    }

    // guess on how many you want to rent
    long long max_value = 0;
    for(int i= 0; i < N; i++){
        long long value = renters_prefix[i];
        long long cow_count = cows_prefix[i];

        auto it = upper_bound(store_prefix.begin(), store_prefix.end(), cow_count);
        int index = it - store_prefix.begin()-1*(it != store_prefix.end());
        value += store_value_prefix[index];
        value += (cow_count - store_prefix[index])*stores[index].cost;

        if (value > max_value){
            max_value = value;
        }
    }
    ofstream fout ("rental.out");
    fout << max_value << "\n";
    return 0;
}