import time 
from datetime import datetime


dd='1532334985'
ff=float(dd)
print(ff)
d1=datetime.utcfromtimestamp(ff)

# d2=datetime.utcfromtimestamp(time.time())
print(time.time())
# d=(d2-d1).days

# print(d)

for i in range(7):
    print(i)