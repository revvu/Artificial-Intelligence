// CSES Problem Set
// Subarray Sums
// Reevu Adakroy 4/7/2021

#include <iostream>

using namespace std;

int n;
int x;


int main(){
    
    cin >> n >> x;
    int arr[n];
    
    for(int i=0; i<n;i++){
        cin>> arr[i];
    }

    int answer = 0;

    int right = 0;
    int left = 1;
    int sum = arr[0];

    while(left<=n){
        if(sum==x){
            answer++;
            left++;
            sum += arr[left];
        }
        else if(sum<x){
            sum+=arr[left];
            left++;
        }
        else{
            sum+=-arr[right];
            right++;
        }
    }
    sum+=-arr[right];
    right++;
    while(right<left){
        if(sum==x){
            answer++;
            left++;
            sum += arr[left];
            break;
        }
        else if(sum<x){
            sum+=arr[left];
            left++;
            break;
        }
        else{
            sum+=-arr[right];
            right++;
        }
    }
    cout << answer << endl;
    return 0;
}