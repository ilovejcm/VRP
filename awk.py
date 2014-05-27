import re
import os

fi = open('or.txt','r')
result = open('result.txt','w')

pattern = '\s'
__id = 0

for i in fi.readlines():
    a = re.split(pattern,i)
    result.write('p'+str(__id)+' = Point('+a[3]+','+a[4]+','+a[2]+','+a[5]+','+a[6]+','+a[7]+','+str(__id)+')')
    result.write(os.linesep)
    result.write('point_list.append(p'+str(__id)+')')
    result.write(os.linesep)
    print 'p'+str(__id)+' = Point('+a[3]+','+a[4]+','+a[2]+','+a[5]+','+a[6]+','+a[7]+','+str(__id)+')'
    print 'point_list.append(p'+str(__id)+')'
    __id += 1    

fi.close()
result.close()

