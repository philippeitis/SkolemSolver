#include <iostream>
#include <algorithm>
#include <ctime>
#include <iomanip>
#include <fstream>

using namespace std;

bool isSkolem(int k, int permutation[]);

int main() {
    const int ColWidth = 24;
    const int ColWidthk = 6;

    // prints things

    cout << setfill(' ') << right
         << setw(ColWidthk) << "k"
         << setw(ColWidth) << "# of sequences"
         << setw(ColWidth) << "computational time"
         << endl;
    cout << setfill('=')
         << setw(ColWidthk) << "="
         << setw(ColWidth) << "="
         << setw(ColWidth) << "="
         << endl;

    int permutation[] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20};

    for(int k = 0; k<13; ++k) {

        int count = 0;
        clock_t begin = clock();

           if(k%4 != 2 && k%4 != 3){
            do {

                if(isSkolem(k,permutation)) {
                    ++count;
                }

            } while ( next_permutation(permutation,permutation+k) );

        }

        clock_t end = clock();
        double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;

        cout << setfill(' ') << right
         << setw(ColWidthk) << k
         << setw(ColWidth) << count
         << setw(ColWidth) << elapsed_secs
         << endl;
    }
    return 0;    
}

bool isSkolem(int k, int permutation[]) {

    int pos = 0;
    bool skolem[2*k]= {false};


    for(int x = 0; x < k; ++x) {
        int perm_num = permutation[x];

        if(skolem[pos+perm_num] || pos+perm_num >= 2*k) {
            return false;
        }

        skolem[pos] = true;
        skolem[pos+perm_num] = true;
        
        while(pos < 2*k && skolem[pos]) {
            ++pos;
        }
    }

    return true;
}

