import argparse, math, time

class entry:
    valid = 0
    tag = 0
    lastAccess = 0
    
debug = 1
    
bsize = 0
nblocks = 0
htime = 0
mtime = 0
assoc = 0
nreads = 0
nhits = 0
nmisses = 0
LRU = False
fname = ''

parser = argparse.ArgumentParser(description='cache simulator arguments')
parser.add_argument('block_size', type=int)
parser.add_argument('num_blocks', type=int)
parser.add_argument('associativity', type=int)
parser.add_argument('hit_time', type=int)
parser.add_argument('miss_time', type=int)
parser.add_argument('LRU', type=bool)
parser.add_argumnet('file_name', type=string)
args = parser.parse_args()

bsize = args.block_size
nblocks = args.num_blocks
assoc = args.associativity
htime = args.hit_time
mtime = args.miss_time
LRU = args.LRU
fname = args.file_name

infile = open(fname, 'r')

addr = 0
setAddr = 0
nSets = nblocks / assoc
setSize = nblocks / nSets
startBlock = 0
minAddr = 0
maxAddr = 0
found = False
wordShift = math.log(bsize, 2)
setShift = math.log(nSets, 2)

if(debug == 1):
    print 'bsize: ' + str(bsize) + '\nnSets: ' + str(nSets)

cache = [temp]
temp = entry()
for i in range(nblocks):
    cache.append(temp)

addr = 0
for line in infile:
    addr = int(line, base=16)
    if(debug == 1):
        print 'Addr: 0x' + hex(addr)
    nreads += 1
    found = False
    setAddr = ( addr / bsize ) % nSets
    startBlock = setAddr * setSize
    endBlock = ( setAddr + 1 ) * setSize - 1
    minAddr = ( addr - ( addr % bsize ) )
    maxAddr = ( addr + ( bsize - addr % bsize ) - 1 )
    if(debug == 1):
        print 'Min Addr: ' + str(minAddr) + ' Max Addr: ' + str(maxAddr)
        print 'Set Addr: ' + str(setAddr)
    
    for i in range(startBlock, endBlock + 1):
        if(cache[i].valid == 1):
            if(cache[i].tag == (addr >> (wordShift + setShift))):
                if(debug == 1):
                    print 'Data found in block: ' + str(i)
                cache[i].lastAccess = time.time()
                found = True
                nhits += 1
                break
    
    if(found == False):
        for i in range(startBlock, endBlock + 1):
            if(cache[i].valid == 0):
                if(debug == 1):
                    print 'Empty block found at ' + str(i)
                cache[i].valid = 1
                cache[i].tag = (addr >> (wordShift + setShift))
                cache[i].lastAccess = time.time()
                found = True
                break
    
    if(found == False):
        if(LRU == False):
            place = random.randint(startBlock, startBlock + setSize - 1)
            if(debug == 1):
                print 'Random block, data stored at ' + str(place)
            cache[place].valid = 1
            cache[place].tag = (addr >> (wordShift + setShift))
            nmisses += 1
        else:
            oldest = startBlock
            oldTime = cache[startBlock].lastAccess
            for i in range(startBlock + 1, endBlock + 1):
                if(cache[i].lastAccess < oldTime):
                    oldTime = cache[i].lastAccess
                    oldest = i
            if(debug == 1):
                print 'Oldest block, data stored at ' + str(oldest)
            cache[oldest].valid = 1
            cache[oldest].tag = (addr >> (wordShift + setShift))
            cache[oldest].lastAccess = time.time()
            nmisses += 1
    
if(debug == 1):
    for i in range(nblocks):
        print 'Block ' + str(i) + ': Valid: ' + str(cache[i].valid) + ' Tag: ' + str(cache[i].tag)

hrate = 0.0
mrate = 0.0
amat = 0.0
hrate = (float(nhits)/nreads) * 100
mrate = (float(nmisses)/nreads) * 100
amat = htime + (mrate / 100) * mtime
print 'Reads: ' + str(nreads)
print 'Hits: ' + str(nhits)
print 'Misses: ' + str(nmisses)
print 'Hit Rate: ' + str(hrate)
print 'Miss Rate: ' + str(mrate)
print 'AMAT: ' + str(amat)

exit()

def is_power2(num):
    return((num & (num - 1)) == 0) and num != 0

class cacheEntry:
    blockNum  = 0
    valid = 0
    
parser = argparse.ArgumentParser(description='cache simulator arguments')
parser.add_argument('word_size', type=int)
parser.add_argument('--L1', nargs=4, type=int, required=True, metavar=('block_size','num_lines','associativity','hit_time'), help='L1 cache parameters')
parser.add_argument('--L2', nargs=4, type=int, required=False, metavar=('block_size','num_lines','associativity','hit_time'), help='L2 cache parameters')
parser.add_argument('--L3', nargs=4, type=int, required=False, metavar=('block_size','num_lines','associativity','hit_time'), help='L3 cache parameters')
parser.add_argument('write_time', type=int)
args = parser.parse_args()

#print args

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
exit()
