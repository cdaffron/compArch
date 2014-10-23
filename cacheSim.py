import argparse, math, time

def is_power2(num):
    return((num & (num - 1)) == 0) and num != 0

class entry:
    valid = 0
    dirty = 0
    tag = 0
    lastAccess = 0
    
parser = argparse.ArgumentParser(description='cache simulator arguments')
parser.add_argument('word_size', type=int)
parser.add_argument('--L1', nargs=4, type=int, required=True, metavar=('block_size','num_lines','associativity','hit_time'), help='L1 cache parameters')
parser.add_argument('--L2', nargs=4, type=int, required=False, metavar=('block_size','num_lines','associativity','hit_time'), help='L2 cache parameters')
parser.add_argument('--L3', nargs=4, type=int, required=False, metavar=('block_size','num_lines','associativity','hit_time'), help='L3 cache parameters')
parser.add_argument('write_time', type=int)
parser.add_argument('file_name', type=str)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--WB', action='store_true')
group.add_argument('--WT', action='store_true')
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
WT = args.WT
WB = args.WB
wordSize = args.word_size
L1bSize = args.L1[0]
L1nBlocks = args.L1[1]
L1hTime = args.L1[3]
memTime = args.write_time
L1assoc = args.L1[2]
L1nReads = 0
L1nHits = 0
L1nMisses = 0
L1nWrites = 0
L2nReads = 0
L2nHits = 0
L2nMisses = 0
L2nWrites = 0
L3nReads = 0
L3nHits = 0
L3nMisses = 0
L3nWrites = 0
MMnWrites = 0
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

# if( WB == True ):
#     print 'You can\'t do that'
#     exit()

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
byteShift = math.log(wordSize, 2)
L1wordShift = math.log(L1bSize, 2)
L1setShift = math.log(L1nSets, 2)
if( numLevels >= 2 ):
    L2wordShift = math.log(L2bSize, 2)
    L2setShift = math.log(L2nSets, 2)
if( numLevels == 3 ):
    L3wordShift = math.log(L3bSize, 2)
    L3setShift = math.log(L3nSets, 2)

if( debug == 1 ):
    print 'L1 bsize: ' + str(L1bSize) + '\nnSets: ' + str(L1nSets)
    
temp = entry()
L1cache = [temp]
for i in range(L1nBlocks):
    temp = entry()
    L1cache.append(temp)

if( numLevels >= 2 ):
    temp = entry()
    L2cache = [temp]
    for i in range(L2nBlocks):
        temp = entry()
        L2cache.append(temp)
        
if( numLevels == 3 ):
    temp = entry()
    L3cache = [temp]
    for i in range(L3nBlocks):
        temp = entry()
        L3cache.append(temp)
    
#L1addr = 0
type = ''
for line in infile:
    separate = line.split()
    addr = int(separate[0], base=16)
    type = str(separate[1])
    if( debug == 1 ):
        print 'Addr: ' + hex(addr)
    
    L1nReads += 1
    L1found = False
    L2found = False
    L3found = False
    L1setAddr = ( ( addr >> int(byteShift) ) / L1bSize ) % L1nSets
    L1startBlock = L1setAddr * L1setSize
    L1endBlock = ( L1setAddr + 1 ) * L1setSize - 1
    L1minAddr = ( addr - ( addr % L1bSize ) )
    L1maxAddr = ( addr + ( L1bSize - addr % L1bSize ) - 1 )
    if( debug == 1 ):
        print 'L1 Min Addr: ' + hex(L1minAddr) + ' Max Addr: ' + hex(L1maxAddr)
        print 'L1 Set Addr: ' + hex(L1setAddr)

    # These are mainly notes for my brain :)
    # Program flow:
    # Look for existing in L1
    # If not, look for existing in L2
    # If not, look for existing in L3
    # If not, look for empty in L3 then do LRU
    # If not, look for empty in L2 then do LRU
    # If not, look for empty in L1 then do LRU
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
            if(L1cache[i].tag == (addr >> int(L1wordShift + L1setShift + byteShift))):
                if( type == 'R' ):
                    if(debug == 1):
                        print 'Data found in L1 block: ' + str(i)
                    L1cache[i].lastAccess = time.time()
                    L1found = True
                    L1nHits += 1
                    break
                if( type == 'W' ):
                    if(debug == 1):
                        print 'Data found and written in L1 block: ' + str(i)
                    L1cache[i].lastAccess = time.time()
                    L1found = True
                    L1nHits += 1
                    L1nWrites += 1
                    L1cache[i].dirty = 1
                    break


    ##################### 
    # L2 Cache Checking #
    #####################
    
    # Logic for finding address in L2 cache.
    if( numLevels >= 2 ):
        if( L1found == False ):
            L2nReads += 1
            L2setAddr = ( ( addr >> int(byteShift) ) / L2bSize ) % L2nSets
            L2startBlock = L2setAddr * L2setSize
            L2endBlock = ( L2setAddr + 1 ) * L2setSize - 1
            L2minAddr = ( addr - ( addr % L2bSize ) )
            L2maxAddr = ( addr + ( L2bSize - addr % L2bSize ) - 1 )
            if( debug == 1 ):
                print 'Heading into L2, address not found in L1 Cache'
                print 'L2 Min Addr: ' + hex(L2minAddr) + ' Max Addr: ' + hex(L2maxAddr)
                print 'L2 Set Addr: ' + hex(L2setAddr)
            for i in range(L2startBlock, L2endBlock + 1):
                # If block valid bit is set, test to see if tag matches address.
                # If match, update block access time.
                if(L2cache[i].valid == 1):
                    if(L2cache[i].tag == (addr >> int(L2wordShift + L2setShift + byteShift))):
                        if(debug == 1):
                            print 'Data found in L2 block: ' + str(i)
                        L2cache[i].lastAccess = time.time()
                        L2found = True
                        L2nHits += 1
                        if( type == 'W' ):
                            L2nWrites += 1
                            L2cache[i].dirty = 1
                        break
        else:
            if( type == 'W' ):
                if( WT == True ):
                    for i in range(L2startBlock, L2endBlock + 1):
                        if(L2cache[i].valid == 1):
                            if(L2cache[i].tag == (addr >> int(L2wordShift + L2setShift + byteShift))):
                                if(debug == 1):
                                    print 'Data found in L2 block: ' + str(i)
                                L2cache[i].lastAccess = time.time()
                                L2found = True
                                L2nHits += 1
                                L2nWrites += 1
                                break


    ##################### 
    # L3 Cache Checking #
    #####################
                        
    # Logic for finding address in L3 cache
    if( numLevels == 3 ):
        if( L1found == False and L2found == False ):
            L3nReads += 1
            L3setAddr = ( ( addr >> int(byteShift) ) / L3bSize ) % L3nSets
            L3startBlock = L3setAddr * L3setSize
            L3endBlock = ( L3setAddr + 1 ) * L3setSize - 1
            L3minAddr = ( addr - ( addr % L3bSize ) )
            L3maxAddr = ( addr + ( L3bSize - addr % L3bSize ) - 1 )
            if( debug == 1 ):
                print 'Heading into L3, address not found in L3 Cache'
                print 'L3 Min Addr: ' + hex(L3minAddr) + ' Max Addr: ' + hex(L3maxAddr)
                print 'L3 Set Addr: ' + hex(L3setAddr)
            for i in range(L3startBlock, L3endBlock + 1):
                # If block valid bit is set, test to see if tag matches address.
                # If match, update block access time.
                if(L3cache[i].valid == 1):
                    if(L3cache[i].tag == (addr >> int(L3wordShift + L3setShift + byteShift))):
                        if(debug == 1):
                            print 'Data found in L3 block: ' + str(i)
                        L3cache[i].lastAccess = time.time()
                        L3found = True
                        L3nHits += 1
                        if( type == 'W' ):
                            L3nWrites += 1
                            L3cache[i].dirty = 1
                        break
        else:
            if( type == 'W' ):
                if( WT == True ):
                    for i in range(L3startBlock, L3endBlock + 1):
                        if(L3cache[i].valid == 1):
                            if(L3cache[i].tag == (addr >> int(L3wordShift + L3setShift + byteShift))):
                                if(debug == 1):
                                    print 'Data found in L3 block: ' + str(i)
                                L3cache[i].lastAccess = time.time()
                                L3found = True
                                L3nHits += 1
                                L3nWrites += 1
                                break

    #####################
    # Main Memory Write #
    #####################
    if( type == 'W' ):
        if( WT == True ):
            MMnWrites += 1

    if( numLevels == 3 ):
        ############################
        # L3 Cache Empty Placement #
        ############################
        
        # Logic for finding empty block to place address.
        if(L1found == False and L2found == False and L3found == False):
            for i in range(L3startBlock, L3endBlock + 1):
                # If empty block found, set valid bit, set tag, set last access time.
                if(L3cache[i].valid == 0):
                    if(debug == 1):
                        print 'Empty L3 block found at ' + str(i)
                    L3cache[i].valid = 1
                    L3cache[i].tag = (addr >> int(L3wordShift + L3setShift + byteShift))
                    L3cache[i].lastAccess = time.time()
                    L3cache[i].dirty = 0
                    L3found = True
                    L3nMisses += 1
                    if( type == 'W' and WT == True ):
                        L3nWrites += 1
                    break
            ## Add LRU here
            if( L3found == False ):
                oldest = L3startBlock
                oldTime = L3cache[L3startBlock].lastAccess
                # Loop through all blocks in the set and find oldest address.
                # Replace with current address, set valid bit, set last access time
                for i in range( L3startBlock + 1, L3endBlock + 1 ):
                    if( L3cache[i].lastAccess < oldTime ):
                        oldTime = L3cache[i].lastAccess
                        oldest = i
                if( debug == 1 ):
                    print 'Oldest L3 block found, data stored at: ' + str(oldest)
                L3cache[oldest].valid = 1
                L3cache[oldest].tag = (addr >> int( L3wordShift + L3setShift + byteShift ) )
                L3cache[oldest].lastAccess = time.time()
                L3nMisses += 1
                if( type == 'W' ):
                    if( WT == True ):
                        L3nWrites += 1
                    if( WB == True ):
                        if( L3cache[oldest].dirty == 1):
                            MMnWrites += 1
                L3cache[oldest].dirty = 0
                L3found = True

    ############################
    # L2 Cache Empty Placement #
    ############################
                    
    if( numLevels >= 2 ):
        # Logic for finding empty block to place address.
        if(L1found == False and L2found == False):
            for i in range(L2startBlock, L2endBlock + 1):
                # If empty block found, set valid bit, set tag, set last access time.
                if(L2cache[i].valid == 0):
                    if(debug == 1):
                        print 'Empty L2 block found at ' + str(i)
                    L2cache[i].valid = 1
                    L2cache[i].tag = (addr >> int(L2wordShift + L2setShift + byteShift))
                    L2cache[i].lastAccess = time.time()
                    L2cache[i].dirty = 0
                    L2found = True
                    L2nMisses += 1
                    if( type == 'W' and WT == True ):
                        L2nWrites += 1
                    break
            if( L2found == False ):
                oldest = L2startBlock
                oldTime = L2cache[L2startBlock].lastAccess
                # Loop through all blocks in the set and find oldest address.
                # Replace with current address, set valid bit, set last access time
                for i in range( L2startBlock + 1, L2endBlock + 1 ):
                    if( L2cache[i].lastAccess < oldTime ):
                        oldTime = L2cache[i].lastAccess
                        oldest = i
                if( debug == 1 ):
                    print 'Oldest L2 block found, data stored at: ' + str(oldest)
                L2cache[oldest].valid = 1
                minOldAddr = ( L2cache[oldest].tag << int( L2wordShift + L2setShift + byteShift ) )
                maxOldAddr = ( minOldAddr | ((1 << (int( L2wordShift + L2setShift + byteShift ))) - 1))
                if( debug == 1 ):
                    print 'minOldAddr: ' + hex(minOldAddr)
                    print 'maxOldAddr: ' + hex(maxOldAddr)
                L2cache[oldest].tag = ( addr >> int( L2wordShift + L2setShift + byteShift ) )
                L2cache[oldest].lastAccess = time.time()
                L2nMisses += 1
                if( type == 'W' ):
                    if( WT == True ):
                        L2nWrites += 1
                    if( WB == True ):
                        if( L2cache[oldest].dirty == 1):
                            ## Write the dirty block to L3 if present
                            if( numLevels == 2):
                                MMnWrites += 1
                            else:
                                for i in range(L3startBlock, L3endBlock + 1):
                                    minBlockAddr = ( L3cache[i].tag << int(L3wordShift + L3setShift + byteShift))
                                    maxBlockAddr = ( minBlockAddr | ((1 << int( L3wordShift + L3setShift + byteShift)) - 1 ) )
                                    if( minOldAddr >= minBlockAddr and maxOldAddr <= maxBlockAddr ):
                                        if( L3cache[i].dirty == 1 ):
                                            MMnWrites += 1
                                        L3cache[i].dirty = 1
                                        L3cache[i].lastAccess = time.time()
                                        break
                        L2cache[oldest].dirty = 0
                L2found = True

    ############################
    # L1 Cache Empty Placement #
    ############################
                    
    # Logic for finding empty block to place address.
    if(L1found == False):
        for i in range(L1startBlock, L1endBlock + 1):
            # If empty block found, set valid bit, set tag, set last access time.
            if(L1cache[i].valid == 0):
                if(debug == 1):
                    print 'Empty L1 block found at ' + str(i)
                L1cache[i].valid = 1
                L1cache[i].tag = (addr >> int(L1wordShift + L1setShift + byteShift))
                L1cache[i].lastAccess = time.time()
                L1cache[i].dirty = 0
                L1found = True
                L1nMisses += 1
                if( type == 'W' and WT == True):
                    L1nWrites += 1
                break
        if( L1found == False ):
            oldest = L1startBlock
            oldTime = L1cache[L1startBlock].lastAccess
            # Loop through all blocks in the set and find oldest address.
            # Replace with current address, set valid bit, set last access time
            for i in range( L1startBlock + 1, L1endBlock + 1 ):
                if( L1cache[i].lastAccess < oldTime ):
                    oldTime = L1cache[i].lastAccess
                    oldest = i
            if( debug == 1 ):
                print 'Oldest L1 block found, data stored at: ' + str(oldest)
            L1cache[oldest].valid = 1
            minOldAddr = ( L1cache[oldest].tag << int( L1wordShift + L1setShift + byteShift ) )
            maxOldAddr = ( minOldAddr | ((1 << (int( L1wordShift + L1setShift + byteShift ))) - 1))
            L1cache[oldest].tag = ( addr >> int( L1wordShift + L1setShift + byteShift ) )
            L1cache[oldest].lastAccess = time.time()
            L1nMisses += 1
            if( type == 'W' ):
                if( WT == True ):
                    L1nWrites += 1
                else:
                    if( L1cache[oldest].dirty == 1 ):
                        if( numLevels == 1 ):
                            MMnWrites += 1
                        elif( numLevels == 2 ):
                            for i in range(L2startBlock, L2endBlock + 1 ):
                                minBlockAddr = ( L2cache[i].tag << int(L2wordShift + L2setShift + byteShift))
                                maxBlockAddr = ( minBlockAddr | ((1 << int( L2wordShift + L2setShift + byteShift)) - 1 ) )
                                if( minOldAddr >= minBlockAddr and maxOldAddr <= maxBlockAddr ):
                                    if( L2cache[i].dirty == 1 ):
                                        MMnWrites += 1
                                    L2cache[i].dirty = 1
                                    L2cache[i].lastAccess = time.time()
                                    break
                        else:
                            for i in range(L2startBlock, L2endBlock + 1 ):
                                minBlockAddr = ( L2cache[i].tag << int(L2wordShift + L2setShift + byteShift))
                                maxBlockAddr = ( minBlockAddr | ((1 << int( L2wordShift + L2setShift + byteShift)) - 1 ) )
                                if( minOldAddr >= minBlockAddr and maxOldAddr <= maxBlockAddr ):
                                    if( L2cache[i].dirty == 1):
                                        minOldAddr = ( L2cache[i].tag << int( L2wordShift + L2setShift + byteShift ) )
                                        maxOldAddr = ( minOldAddr | ((1 << (int( L2wordShift + L2setShift + byteShift ))) - 1))
                                        for j in range(L3startBlock, L3endBlock + 1 ):
                                            minBlockAddr = ( L3cache[j].tag << int(L3wordShift + L3setShift + byteShift))
                                            maxBlockAddr = ( minBlockAddr | ((1 << int( L3wordShift + L3setShift + byteShift)) - 1 ) )
                                            if( minOldAddr >= minBlockAddr and maxOldAddr <= maxBlockAddr ):
                                                if( L3cache[j].dirty == 1 ):
                                                    MMnWrites += 1
                                                L3cache[j].dirty = 1
                                                L3cache[j].lastAccess = time.time()
                                                break
                                    L2cache[i].dirty = 1
                                    L2cache[i].lastAccess = time.time()
                                    break

                    L1cache[oldest].dirty = 1
                    L1cache[oldest].lastAccess = time.time()

            L1found = True
      
if(debug == 1):
    print 'L1 Cache Contents:'
    for i in range(L1nBlocks):
        print 'Block ' + str(i) + ': Valid: ' + str(L1cache[i].valid) + ' Tag: ' + str(L1cache[i].tag)
        
    if( numLevels >= 2 ):
        print 'L2 Cache Contents:'
        for i in range(L2nBlocks):
            print 'Block ' + str(i) + ': Valid: ' + str(L2cache[i].valid) + ' Tag: ' + str(L2cache[i].tag)
            
    if( numLevels == 3 ):
        print 'L3 Cache Contents:'
        for i in range(L3nBlocks):
            print 'Block ' + str(i) + ': Valid: ' + str(L3cache[i].valid) + ' Tag: ' + str(L3cache[i].tag)

# Output results
L1hrate = (float(L1nHits)/L1nReads) * 100
L1mrate = (float(L1nMisses)/L1nReads) * 100
if( numLevels >= 2 ):
    L2hrate = (float(L2nHits)/L2nReads) * 100
    L2mrate = (float(L2nMisses)/L2nReads) * 100
if( numLevels == 3 ):
    L3hrate = (float(L3nHits)/L3nReads) * 100
    L3mrate = (float(L3nMisses)/L3nReads) * 100
if( numLevels == 1 ):
    amat = L1hTime + (L1mrate / 100) * memTime
if( numLevels == 2 ):
    amat = L1hTime + (L1mrate / 100) * (L2hTime + (L2mrate / 100) * memTime)
if( numLevels == 3 ):
    amat = L1hTime + (L1mrate / 100) * (L2hTime + (L2mrate / 100) * (L3hTime + (L3mrate / 100) * memTime))
print 'L1 Reads: ' + str(L1nReads)
print 'L1 Hits: ' + str(L1nHits)
print 'L1 Misses: ' + str(L1nMisses)
if( numLevels >= 2 ):
    print 'L2 Reads: ' + str(L2nReads)
    print 'L2 Hits: ' + str(L2nHits)
    print 'L2 Misses: ' + str(L2nMisses)
if( numLevels == 3 ):
    print 'L3 Reads: ' + str(L3nReads)
    print 'L3 Hits: ' + str(L3nHits)
    print 'L3 Misses: ' + str(L3nMisses)
print 'L1 Hit Rate: ' + str(L1hrate)
print 'L1 Miss Rate: ' + str(L1mrate)
if( numLevels >= 2 ):
    print 'L2 Hit Rate: ' + str(L2hrate)
    print 'L2 Miss Rate: ' + str(L2mrate)
if( numLevels == 3 ):
    print 'L3 Hit Rate: ' + str(L3hrate)
    print 'L3 Miss Rate: ' + str(L3mrate)
print 'AMAT: ' + str(amat)