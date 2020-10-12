#include <iostream>
#include <ctime>
#include <algorithm>
// #include <fstream>
// #include <string>

int main() {
    const int ColWidth = 24;
    const int ColWidthk = 6;

    // prints things

    std::cout << "k, # of sequences, computational time" << std::endl;

    int permutation[] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20};
//    std::string numberWords[] = {"0","1","2","3","4","5","6","7","8","9","10","11","12","13"};
    for(register unsigned int k = 12; k<13; ++k) {

        int count = 0;
        clock_t begin = clock();


           if(k%4 != 2 && k%4 != 3){
/*                std::string filename = "tskolemdata";
                filename.append(numberWords[k]);
                filename.append(".txt");
                std::ofstream fileoutput;
               fileoutput.open(filename);
*/
// 455936

                do {
                    if(permutation[0]==permutation[1]+1 || permutation[-1]==permutation[-2]+1){}
                
                    else{
                    register unsigned int trials = 0;
                    register unsigned int pos = 0;
                    bool skolem[2*k]= {false};

                    for (register unsigned int x = 0; x < k; ++x) {

                        if(skolem[pos+permutation[x]] || pos+permutation[x] >= 2*k) {
                            break;
                        }

                        skolem[pos] = true; skolem[pos+permutation[x]] = true;
                        
                        while(skolem[pos]) {
                            ++pos;
                        }

                        ++trials;

                    }

                    if(trials==k){
                        ++count;
/*                        fileoutput << "[" << permutation[0];
                        for(int i=1; i<k;++i){
                            fileoutput << ", " << permutation[i];
                        }
                        fileoutput << "]" << std::endl;
*/                    }

                    }
            } while (std::next_permutation(permutation,permutation+k));

//            fileoutput.close();
        }

        clock_t end = clock();
        double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;

        std::cout << k << ", " << count << ", " << elapsed_secs << std::endl;
    }

    return 0;    
}

