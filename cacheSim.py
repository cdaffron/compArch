
def is_power2(num):
    return((num & (num - 1)) == 0) and num != 0

class cacheEntry:
    blockNum  = 0
    valid = 0
    

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