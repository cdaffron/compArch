#include <iostream>
#include <fstream>
#include <cstdlib>
#include <cstdio>
#include <vector>
#include <cmath>
#include <ctime>
#include <string>

using namespace std;

/*Global variable used for testing
  and debugging purposes, set to 
  1 if verbose output is desired
*/

#define DEBUG 1



/*Class for holding a cache block entry*/
class entry {
	public:
		int valid;
		int tag;
		time_t lastAccess;
		entry();
};

entry::entry() {
	valid = 0;
	tag = 0;
}



/* Argument format: block size, number of blocks, associativity, 
   hit time, miss time, LRU, datafile name */
int main(int argc, char **argv) {
	
	
	int bsize;
	int nblocks;
	int htime;
	int mtime;
	int assoc;
	int nreads = 0;
	int nhits = 0;
	int nmisses = 0;
	bool LRU;
	string fname;

	/*Parse command line arguments*/
	if(argc == 8) {
		bsize = atoi(argv[1]);
		nblocks = atoi(argv[2]);
		assoc = atoi(argv[3]);
		htime = atoi(argv[4]);
		mtime = atoi(argv[5]);
		if(atoi(argv[6]) == 1) {
			LRU = true;
		} else {
			LRU = false;
		}
		fname = argv[7];
	} else {
		printf("Argument format: ./cache block_size, number_of_blocks, associativity, hit_time, miss_time, LRU, datafile_name\n");
		printf("Using default values\n");
		bsize = 1;
		nblocks = 8;
		htime = 1;
		mtime = 10;
		assoc = 1;
		LRU = false;
		fname = "input.txt";
	}


	cout << "fname: " << fname << endl;


	/*Open input file and test for errors*/
	ifstream file;
	file.open(fname.c_str(), ifstream::in);

	if(!file.is_open()) {
		cout << "File " << fname << " not found!!" << endl;
		exit(1);
	}


	int addr;
	int setAddr; 
	int nSets = nblocks / assoc;
	int setSize = nblocks / nSets;
	int startBlock;
	int endBlock;
	int minAddr;
	int maxAddr;
	bool found = false;
	int wordShift = log10(bsize)/log10(2);
	int setShift = log10(nSets)/log10(2);

	if(DEBUG) printf("bsize: %d\nnSets: %d\n", bsize, nSets);

	vector<entry> cache (nblocks);

	/*Read input file addresses*/
	while(!file.eof()) {
		file >> hex >> addr;
		
		if(!file.eof()) {
			if(DEBUG) printf("Addr: 0x%x (%d)\n", addr, addr);
			nreads++;
			found = false;
			setAddr = (addr/bsize) % nSets;
			startBlock = setAddr * setSize;
			endBlock = (setAddr + 1) * setSize - 1;
			minAddr = (addr - (addr % bsize));
			maxAddr = (addr + (bsize - addr % bsize) - 1);
			
			/*Print debug info of DEBUG is set to 1*/
			if(DEBUG) printf("Min Addr: %d\nMax Addr: %d\n", minAddr, maxAddr);
			if(DEBUG) printf("(%d / %d) %% %d\n", addr, bsize, nSets);
			if(DEBUG) cout << "Set address: " << setAddr << endl;

			/*Check to see if data is in cache*/
			for(int i = startBlock; i <= endBlock; i++) {
				if(cache[i].valid == 1) {
					if(cache[i].tag == (addr >> (wordShift + setShift))) {
						if(DEBUG) printf("Data found in block %d\n", i);
						cache[i].lastAccess = time(NULL);
						found = true;
						nhits++;
						break;
					}
				}
			}

			/*If data is not in cache*/
			if(!found) {
				/*Search for an empty block*/
				for(int i = startBlock; i <= endBlock; i++) {
					if(cache[i].valid == 0) {
						if(DEBUG) printf("Empty block found at %d\n", i);
						cache[i].valid = 1;
						cache[i].tag = (addr >> (wordShift + setShift));
						cache[i].lastAccess = time(NULL);
						found = true;
						nmisses++;
						break;
					}
				}
			}
			
			/*If no empty blocks replace using specified policy*/
			if(!found) {
				if(!LRU) {
					int place = (rand() % setSize) + startBlock;
					if(DEBUG) printf("Random block, data stored at %d\n", place);
					cache[place].valid = 1;
					cache[place].tag = (addr >> (wordShift + setShift));
					nmisses++;
				} else {
					int oldest = startBlock;
					time_t oldTime = cache[startBlock].lastAccess;
					for(int i = (startBlock + 1); i <= endBlock; i++) {
						if(cache[i].lastAccess < oldTime) {
							oldTime = cache[i].lastAccess;
							oldest = i;
						}
					}
					if(DEBUG) printf("Oldest block, data stored at %d\n", oldest);
					cache[oldest].valid = 1;
					cache[oldest].tag = (addr >> (wordShift + setShift));
					cache[oldest].lastAccess = time(NULL);
					nmisses++;
				}
			}
		}
	}

	if(DEBUG) {
		for(int i = 0; i < nblocks; i++) {
			printf("Block %d: Valid: %d Tag: %d\n", i, cache[i].valid, cache[i].tag);
		}
	}

	float hrate;
	float mrate;
	float amat;
	hrate = ((float)nhits/nreads)*100;
	mrate = ((float)nmisses/nreads)*100;
	amat = htime + (mrate/100)*mtime;
	printf("Reads: %d\n", nreads);
	printf("Hits: %d\n", nhits);
	printf("Misses: %d\n", nmisses);
	printf("Hit Rate: %.2f%%\n", hrate);
	printf("Miss Rate: %.2f%%\n", mrate);
	printf("AMAT: %.2f\n", amat);
	return 0;

}



