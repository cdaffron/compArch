import argparse

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

wordSize = input('Enter Word Size: ')
#if( wordSize == 0 or ((wordSize & (wordSize - 1)) != 0)):
if not is_power2(wordSize):
    print 'Word size must be a power of 2'
    exit()
numLevels = input('Enter number of levels of cache: ')
if( numLevels < 1 or numLevels > 3):
    print 'There must be 1-3 levels of cache'
    exit()
blockSize = input('Enter Block Size: ')
lines = input('Enter Number of Lines: ')
assoc = input('Enter Associativity: ')
if( assoc > lines ):
    print 'Cannot have higher associativity than number of lines'
    exit()

print 'L1 cache stats:'
hitTimeL1 = input('    Enter hit time: ')
missTimeL1 = input('    Enter miss time: ')

if( numLevels > 1):
    print 'L2 cache stats: '
    hitTimeL2 = input('    Enter hit time: ')
    missTimeL2 = input('    Enter miss time: ')

if( numLevels > 2):
    print 'L3 cache stats: '
    hitTimeL3 = input('    Enter hit time: ')
    missTimeL3 = input('    Enter miss time: ')
    
writeToMem = input('Enter write time to memory: ')