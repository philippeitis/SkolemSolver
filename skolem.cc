#include <iostream>
#include <ctime>
#include <algorithm>


int main() {
    
    std::cout << "k, # of sequences, computational time" << std::endl;

    int permutation[] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20};

    for(register unsigned int k = 0; k<14; ++k) {

        int count = 0;
        clock_t begin = clock();

           if(k%4 != 2 && k%4 != 3){

                do {
                    // Even putting ints before the arrays to save memory (I think)
                    // register unsigned ints! look at how fancy i am
                    register unsigned int trials = 0;
                    register unsigned int pos = 0;
                    bool skolem[2*k]= {false};

                    for (register unsigned int x = 0; x < k; ++x) {

                        // This checks if the element of the list that we want to check is occupied
                        if(skolem[pos+permutation[x]] || pos+permutation[x] >= 2*k) {
                            break;
                        }

                        skolem[pos] = true; skolem[pos+permutation[x]] = true;
                        
                        while(skolem[pos]) {
                            ++pos;
                        }

                        ++trials;

                    }

                    // We don't need the array for this - we just need to know if the program has gone through all
                    // the steps, like it should have
                    if(trials==k){++count;}

            } while (std::next_permutation(permutation,permutation+k));
        }

        clock_t end = clock();
        double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;

        std::cout << k << ", " << count << ", " << elapsed_secs << std::endl;
    }

    return 0;    
}
