f = open("continuous.txt", 'w')
for x in xrange(0,1000000):
  f.write(hex(x).lstrip("0x").zfill(8) + " R\n")
f.close

f = open("evens.txt", 'w')
for x in xrange(0,1000000):
  if x%2==0:
    f.write(hex(x).lstrip("0x").zfill(8) + " R\n")
f.close

f = open("byFours.txt", 'w')
for x in xrange(0,1000000):
  if x%4==0:
    f.write(hex(x).lstrip("0x").zfill(8) + " R\n")
f.close
