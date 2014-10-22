import argparse, math, time

def is_power2(num):
    return((num & (num - 1)) == 0) and num != 0

class entry:
    valid = 0
    tag = 0
    lastAccess = 0
    
parser = argparse.ArgumentParser(description='cache simulator arguments')
parser.add_argument('word_size', type=int)
parser.add_argument('--L1', nargs=4, type=int, required=True, metavar=('block_size','num_lines','associativity','hit_time'), help='L1 cache parameters')
parser.add_argument('--L2', nargs=4, type=int, required=False, metavar=('block_size','num_lines','associativity','hit_time'), help='L2 cache parameters')
parser.add_argument('--L3', nargs=4, type=int, required=False, metavar=('block_size','num_lines','associativity','hit_time'), help='L3 cache parameters')
parser.add_argument('write_time', type=int)
parser.add_argument('file_name', type=str)
args = parser.parse_args()

#print args

print 'File name: ' + args.file_name
print 'Word size is: ' + str(args.word_size)
print 'Write to memory delay is: ' + str(args.write_time)
print 'L1 stats:'
print '\tBlock Size: ' + str(args.L1[0])
print '\tNumber of Lines: ' + str(args.L1[1])
print '\tAssociativity: ' + str(args.L1[2])
print '\tHit Time: ' + str(args.L1[3])
if( args.L2 ):
    print 'L2 stats:'
    print '\tBlock Size: ' + str(args.L2[0])
    print '\tNumber of Lines: ' + str(args.L2[1])
    print '\tAssociativity: ' + str(args.L2[2])
    print '\tHit Time: ' + str(args.L2[3])
if( args.L3 ):
    print 'L3 stats:'
    print '\tBlock Size: ' + str(args.L3[0])
    print '\tNumber of Lines: ' + str(args.L3[1])
    print '\tAssociativity: ' + str(args.L3[2])
    print '\tHit Time: ' + str(args.L3[3])

debug = 1
numLevels = 1
L1bSize = args.L1[0]
L1nBlocks = args.L1[1]
L1hTime = args.L1[3]
memTime = args.write_time
L1assoc = args.L1[2]
L1nReads = 0
L1nHits = 0
L1nMisses = 0
L2nReads = 0
L2nHits = 0
L2nMisses = 0
L3nReads = 0
L3nHits = 0
L3nMisses = 0
fname = args.file_name
if( args.L2 ):
    numLevels = 2
    L2bSize = args.L2[0]
    L2nBlocks = args.L2[1]
    L2hTime = args.L2[3]
    L2assoc = args.L2[2]
if( args.L3 ):
    if( not args.L2 ):
        print 'Cannot have L3 without L2'
        exit()
    numLevels = 3
    L3bSize = args.L3[0]
    L3nBlocks = args.L3[1]
    L3hTime = args.L3[3]
    L3assoc = args.L3[2]

infile = open(fname, 'r')

addr = 0
L1setAddr = 0
L2setAddr = 0
L3setAddr = 0
L1nSets = L1nBlocks / L1assoc
L1setSize = L1nBlocks / L1nSets
if( numLevels >= 2 ):
    L2nSets = L2nBlocks / L2assoc
    L2setSize = L2nBlocks / L2nSets
if( numLevels == 3 ):
    L3nSets = L3nBlocks / L3assoc
    L3setSize = L3nBlocks / L3nSets
    
L1startBlock = 0
L2startBlock = 0
L3startBlock = 0
L1minAddr = 0
L2minAddr = 0
L3minAddr = 0
L1maxAddr = 0
L2maxAddr = 0
L3maxAddr = 0
L1found = False
L2found = False
L3found = False
L1wordShift = math.log(L1bSize, 2)
L1setShift = math.log(L1nSets, 2)

if( debug == 1 ):
    print 'L1 bsize: ' + str(L1bSize) + '\nnSets: ' + str(L1nSets)
    
temp = entry()
L1cache = [temp]
for i in range(L1nBlocks):
    temp = entry()
    L1cache.append(temp)
    
L1addr = 0
type = ''
for line in infile:
    separate = line.split()
    L1addr = int(separate[0], base=16)
    type = str(separate[1])
    if( debug == 1 ):
        print 'Addr: ' + hex(L1addr)
    L1nReads += 1
    L1found = False
    L2found = False
    L3found = False
    L1setAddr = ( addr / L1bSize ) % L1nSets
    L1startBlock = L1setAddr * L1setSize
    L1endBlock = ( L1setAddr + 1 ) * L1setSize - 1
    L1minAddr = ( L1addr - ( L1addr % L1bSize ) )
    L1maxAddr = ( L1addr + ( L1bSize - L1addr % L1bSize ) - 1 )
    if( debug == 1 ):
        print 'L1 Min Addr: ' + hex(L1minAddr) + ' Max Addr: ' + hex(L1maxAddr)
        print 'L1 Set Addr: ' + hex(L1setAddr)

    # These are mainly notes for my brain :)
    # Program flow:
    # Look for existing in L1
    # If not, look for empty in L1
    # If not, look for existing in L2
    # If not, look for empty in L2
    # If not, look for existing in L3
    # If not, look for empty in L3
    # If not...
    # LRU write to L3
    # LRU write to L2
    # LRU write to L1

    ##################### 
    # L1 Cache Checking #
    #####################

    # Logic for finding address in L1 cache.
    for i in range(L1startBlock, L1endBlock + 1):
        # If block valid bit is set, test to see if tag matches address.
        # If match, update block access time.
        if(L1cache[i].valid == 1):
            if(L1cache[i].tag == (L1addr >> int(L1wordShift + L1setShift))):
                if(debug == 1):
                    print 'Data found in L1 block: ' + str(i)
                L1cache[i].lastAccess = time.time()
                L1found = True
                L1nHits += 1
                break
    
    # Logic for finding empty block to place address.
    if(L1found == False):
        for i in range(L1startBlock, L1endBlock + 1):
            # If empty block found, set valid bit, set tag, set last access time.
            if(L1cache[i].valid == 0):
                if(debug == 1):
                    print 'Empty L1 block found at ' + str(i)
                L1cache[i].valid = 1
                L1cache[i].tag = (L1addr >> int(L1wordShift + L1setShift))
                L1cache[i].lastAccess = time.time()
                L1found = True
                L1nMisses += 1
                break

    ##################### 
    # L2 Cache Checking #
    #####################

    # Logic for finding address in L2 cache.
    if(L1found == False and L2found == False):
        L2setAddr = ( addr / L2bSize ) % L2nSets
        L2startBlock = L2setAddr * L2setSize
        L2endBlock = ( L2setAddr + 1 ) * L2setSize - 1
        L2minAddr = ( L2addr - ( L2addr % L2bSize ) )
        L2maxAddr = ( L2addr + ( L2bSize - L2addr % L2bSize ) - 1 )
        if( debug == 1 ):
            print 'Heading into L2, address not found in L1 Cache'
            print 'L2 Min Addr: ' + hex(L2minAddr) + ' Max Addr: ' + hex(L2maxAddr)
            print 'L2 Set Addr: ' + hex(L2setAddr)
        for i in range(L2startBlock, L2endBlock + 1):
            # If block valid bit is set, test to see if tag matches address.
            # If match, update block access time.
            if(L2cache[i].valid == 1):
                if(L2cache[i].tag == (L1addr >> int(L1wordShift + L1setShift))):
                    if(debug == 1):
                        print 'Data found in L2 block: ' + str(i)
                    L2cache[i].lastAccess = time.time()
                    L2found = True
                    L2nHits += 1
                    break
    
    # Logic for finding empty block to place address.
    if(L1found == False and L2found == False):
        for i in range(L2startBlock, L2endBlock + 1):
            # If empty block found, set valid bit, set tag, set last access time.
            if(L2cache[i].valid == 0):
                if(debug == 1):
                    print 'Empty L2 block found at ' + str(i)
                L2cache[i].valid = 1
                L2cache[i].tag = (L1addr >> int(L1wordShift + L1setShift))
                L2cache[i].lastAccess = time.time()
                L2found = True
                L2nMisses += 1
                break

    ##################### 
    # L3 Cache Checking #
    #####################

    # Logic for finding address in L3 cache.
    if(L1found == False and L2found == False and L3found == False):
        L3setAddr = ( addr / L3bSize ) % L3nSets
        L3startBlock = L3setAddr * L3setSize
        L3endBlock = ( L3setAddr + 1 ) * L3setSize - 1
        L3minAddr = ( L3addr - ( L3addr % L3bSize ) )
        L3maxAddr = ( L3addr + ( L3bSize - L3addr % L3bSize ) - 1 )
        if( debug == 1 ):
            print 'Heading into L3, address not found in L3 Cache'
            print 'L3 Min Addr: ' + hex(L3minAddr) + ' Max Addr: ' + hex(L3maxAddr)
            print 'L3 Set Addr: ' + hex(L3setAddr)
        for i in range(L3startBlock, L3endBlock + 1):
            # If block valid bit is set, test to see if tag matches address.
            # If match, update block access time.
            if(L3cache[i].valid == 1):
                if(L3cache[i].tag == (L1addr >> int(L1wordShift + L1setShift))):
                    if(debug == 1):
                        print 'Data found in L3 block: ' + str(i)
                    L3cache[i].lastAccess = time.time()
                    L3found = True
                    L3nHits += 1
                    break
    
    # Logic for finding empty block to place address.
    if(L1found == False and L2found == False and L3found == False):
        for i in range(L3startBlock, L3endBlock + 1):
            # If empty block found, set valid bit, set tag, set last access time.
            if(L3cache[i].valid == 0):
                if(debug == 1):
                    print 'Empty L3 block found at ' + str(i)
                L3cache[i].valid = 1
                L3cache[i].tag = (L1addr >> int(L1wordShift + L1setShift))
                L3cache[i].lastAccess = time.time()
                L3found = True
                L3nMisses += 1
                break

    ############# 
    # LRU Write #
    #############

    # Logic for replacing LRU block with address.
    if(L1found == False):
        oldest = L1startBlock
        oldTime = L1cache[L1startBlock].lastAccess
        # Loop through all blocks in set and find oldest address.
        # Replace with curr address, set valid bit, set last access time.
        for i in range(L1startBlock + 1, L1endBlock + 1):
            if(L1cache[i].lastAccess < oldTime):
                oldTime = L1cache[i].lastAccess
                oldest = i
        if(debug == 1):
            print 'Oldest L1 block, data stored at: ' + str(oldest)
        L1cache[oldest].valid = 1
        L1cache[oldest].tag = (L1addr >> int(L1wordShift + L1setShift))
        L1cache[oldest].lastAccess = time.time()
        L1nMisses += 1
        
if(debug == 1):
    for i in range(L1nBlocks):
        print 'Block ' + str(i) + ': Valid: ' + str(L1cache[i].valid) + ' Tag: ' + str(L1cache[i].tag)

# Output results
hrate = 0.0
mrate = 0.0
amat = 0.0
hrate = (float(L1nHits)/L1nReads) * 100
mrate = (float(L1nMisses)/L1nReads) * 100
amat = L1hTime + (mrate / 100) * memTime
print 'Reads: ' + str(L1nReads)
print 'Hits: ' + str(L1nHits)
print 'Misses: ' + str(L1nMisses)
print 'Hit Rate: ' + str(hrate)
print 'Miss Rate: ' + str(mrate)
print 'AMAT: ' + str(amat)