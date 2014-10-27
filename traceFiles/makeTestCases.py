import random

f = open("spatialLocality.txt", 'w')
for x in xrange(0,1048576):
  if random.randint(1, 2)%2==0:
    f.write(hex(x).lstrip("0x").zfill(8) + " R\n")
  else:
    f.write(hex(x).lstrip("0x").zfill(8) + " W\n")  
f.close

f = open("temporalLocality.txt", 'w')
for x in xrange(0,256):
  for y in xrange(0,256):
    if random.randint(1, 2)%2==0:
      f.write(hex(y).lstrip("0x").zfill(8) + " R\n")
    else:
      f.write(hex(y).lstrip("0x").zfill(8) + " W\n")  
f.close

f = open("disparate.txt", 'w')
for x in xrange(1,1048576):
  if random.randint(1, 2)%2==0:
    f.write(hex(random.randrange(0,4294967296)).lstrip("0x").zfill(8) + " R\n")
  else:
    f.write(hex(random.randrange(0,4294967296)).lstrip("0x").zfill(8) + " W\n")
f.close

######################################################################
# Old test files, decided it didn't make much sense to test that way #
######################################################################

# f = open("readContinuous.txt", 'w')
# for x in xrange(0,1048576):
#   f.write(hex(x).lstrip("0x").zfill(8) + " R\n")
# f.close

# f = open("readByTwos.txt", 'w')
# for x in xrange(0,1048576):
#   if x%2==0:
#     f.write(hex(x).lstrip("0x").zfill(8) + " R\n")
# f.close

# f = open("readByFours.txt", 'w')
# for x in xrange(0,1048576):
#   if x%4==0:
#     f.write(hex(x).lstrip("0x").zfill(8) + " R\n")
# f.close

# f = open("readByEights.txt", 'w')
# for x in xrange(0,1048576):
#   if x%8==0:
#     f.write(hex(x).lstrip("0x").zfill(8) + " R\n")
# f.close

# f = open("readBySixteens.txt", 'w')
# for x in xrange(0,1048576):
#   if x%16==0:
#     f.write(hex(x).lstrip("0x").zfill(8) + " R\n")
# f.close

# f = open("writeContinuous.txt", 'w')
# for x in xrange(0,1048576):
#   f.write(hex(x).lstrip("0x").zfill(8) + " W\n")
# f.close

# f = open("writeByTwos.txt", 'w')
# for x in xrange(0,1048576):
#   if x%2==0:
#     f.write(hex(x).lstrip("0x").zfill(8) + " W\n")
# f.close

# f = open("writeByFours.txt", 'w')
# for x in xrange(0,1048576):
#   if x%4==0:
#     f.write(hex(x).lstrip("0x").zfill(8) + " W\n")
# f.close

# f = open("writeByEights.txt", 'w')
# for x in xrange(0,1048576):
#   if x%8==0:
#     f.write(hex(x).lstrip("0x").zfill(8) + " W\n")
# f.close

# f = open("writeBySixteens.txt", 'w')
# for x in xrange(0,1048576):
#   if x%16==0:
#     f.write(hex(x).lstrip("0x").zfill(8) + " W\n")
# f.close

# f = open("alternateContinuous.txt", 'w')
# for x in xrange(0,1048576):
#   if random.randint(1, 2)%2==0:
#     f.write(hex(x).lstrip("0x").zfill(8) + " R\n")
#   else:
#     f.write(hex(x).lstrip("0x").zfill(8) + " W\n")  
# f.close

# f = open("alternateByTwos.txt", 'w')
# for x in xrange(0,1048576):
#   if x%2==0:
#     if random.randint(1, 2)%2==0:
#       f.write(hex(x).lstrip("0x").zfill(8) + " R\n")
#     else:
#       f.write(hex(x).lstrip("0x").zfill(8) + " W\n")
# f.close

# f = open("alternateByFours.txt", 'w')
# for x in xrange(0,1048576):
#   if x%4==0:
#     if random.randint(1, 2)%2==0:
#       f.write(hex(x).lstrip("0x").zfill(8) + " R\n")
#     else:
#       f.write(hex(x).lstrip("0x").zfill(8) + " W\n")
# f.close

# f = open("alternateByEights.txt", 'w')
# for x in xrange(0,1048576):
#   if x%8==0:
#     if random.randint(1, 2)%2==0:
#       f.write(hex(x).lstrip("0x").zfill(8) + " R\n")
#     else:
#       f.write(hex(x).lstrip("0x").zfill(8) + " W\n")
# f.close

# f = open("alternateBySixteens.txt", 'w')
# for x in xrange(0,1048576):
#   if x%16==0:
#     if random.randint(1, 2)%2==0:
#       f.write(hex(x).lstrip("0x").zfill(8) + " R\n")
#     else:
#       f.write(hex(x).lstrip("0x").zfill(8) + " W\n")
# f.close

# f = open("random.txt", 'w')
# for x in xrange(1,1048576):
#   if random.randint(1, 2)%2==0:
#     f.write(hex(random.randrange(0,4294967296)).lstrip("0x").zfill(8) + " R\n")
#   else:
#     f.write(hex(random.randrange(0,4294967296)).lstrip("0x").zfill(8) + " W\n")
# f.close
