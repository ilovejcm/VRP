# -*- coding: cp936 -*-
import random
import math
import copy
import operator

class Point(object):
    def __init__(self,x,y,weight,work_time,et,lt,point_id):
        self.x = x
        self.y = y
        self.weight = weight
        self.work_time = work_time
        self.et = et
        self.lt = lt
        self.id = point_id

class Static(object):
    MAX_WEIGHT_FOR_CAR = 30
    CAR_SPEED = 70
    MAX = 1000000
    C = 50
    MAX_CAR = 7
    HAS_CENTER = 6
    EARLIST_TIME = 6
    LAST_TIME = 18

    Q = 1   
    WEIGHT_FOR_INFO = 3     
    WEIGHT_FOR_QIFA = 9     
    LOSE_INFO = 0.5         
    #POINT_NUMBER = 78       
    
    @staticmethod
    def distance(point1,point2,point_list):
        point_1 = point_list[int(point1)-1]
        point_2 = point_list[int(point2)-1]
        x1 = point_1.x
        y1 = point_1.y
        x2 = point_2.x
        y2 = point_2.y
        return math.sqrt( pow(x1-x2,2)+pow(y1-y2,2) )
    


def update():
    information = [ [i*(1-Static.LOSE_INFO) for i in information[j]] for j in range(len(information)) ] 


class Ant_Colony(object):
    def __init__(self):
        self.route = list()
        self.child = list()
        i = 0
        while (i < Static.MAX_CAR):
            child = Ant(point_list)
            self.child.append(child)
            i += 1

    def lets_crazy(self,point_list):
        home = 0
        pltemp = range(0,Static.HAS_CENTER)
        for i in self.child:
            print "new :"
            cent = i.chose_start_center(pltemp)
            pltemp.remove(cent)
            while (i.time < Static.LAST_TIME):
                temp = i.time
                weight = i.weight
                while (i.weight < Static.MAX_WEIGHT_FOR_CAR):
                    one = i.chose_direct(point_list,self.route)
                    #print '#######################################'
                    #print one
                    i.route.append(one)
                    print i.route
                    i.weight += point_list[one].weight

                #i.route.pop()
                home = i.go_home(point_list)
                #print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                if home == -1:
                    while(self.route[len(self.route)-1] not in [0,1,2,3,4,5]):
                        self.route.pop()
                    i.time = temp
                    i.weight = weight
                    break 
                else:
                    i.route.append(home)
                    self.route.append(home)
                    i.time = i.time + point_list[i.route[len(i.route)-1]].work_time + Static.distance(i.route[len(i.route)-1],home,point_list) / Static.CAR_SPEED
                    i.weight = 0
##                print 'home is:   '+ str(home)
##                print 'ii time is:   '
##                print i.time


class Ant(Ant_Colony):
    def __init__(self,point_list):
        #self.forbiden = list()
        self.route = list()
        #self.chose_start_center(point_list)
        self.weight = 0
        self.earlist_time = Static.EARLIST_TIME
        self.time = self.earlist_time

    def chose_start_center(self,point_list):
        rand = random.choice(point_list)
        #print type(rand)
        self.route.append(rand)
        return rand

    
    def travel(self,Point_list):
        i = 0
        travel_sum = 0
        while( i<len(self.rout)-1 ): 
            dis = self.distance( Point_list[self.rout[i]],Point_list[self.rout[i+1]],point_list)
            travel_sum += dis*3*1.3
            i += 1
        return travel_sum

    def time_window(self,point1,point2,Point_list):
        print 'point1: '+str(point1) + '  point2: '+ str(point2)
        self.time = self.earlist_time
        self.cost = 0
        #self.extra_car = 0
        i = 0
        #print self.rout[i]
        #print self.rout[i+1]
        self.temp_time = self.time + Point_list[point1].work_time + Static.distance(point1,point2,point_list) / Static.CAR_SPEED
        #print Point_list[self.rout[i+1]].work_time
        self.time = self.temp_time
##        print 'self.time is'
##        print self.time
##        print 'Point_list[point2].et is: '
##        print Point_list[point2].et
##        print 'Point_list[point2].lt is: '
##        print Point_list[point2].lt
        if self.time > 18:
        #    print '>18'
            self.extra_car = self.extra_car + 1
            self.time = self.earlist_time
            self.cost = -1
            return -1
        elif self.time < ( Point_list[point2-1].et - 2 ) or self.time > ( Point_list[point2-1].lt + 2 ):
         #   print '1'
            self.cost = Static.MAX
            return Static.MAX

#print self.rout
#print Point_list[self.rout[i]].id,'  and  ',Point_list[self.rout[i+1]].id,'is our of time'
#print self.temp_time
#print 'et-2 is:',Point_list[self.rout[i+1]].et - 2
#print 'lt + 2is:',Point_list[self.rout[i+1]].lt + 2
#print 'OUT'''
        elif self.time < (Point_list[point2-1].et):
          #  print '2'
            self.cost += abs(Point_list[point2-1].et - self.time) * Static.C
        elif self.time > (Point_list[point2-1].lt):
           # print '3'
            self.cost += abs(Point_list[point2-1].lt - self.time) * Static.C
        #print 'self time is'
        #print self.time
        return self.cost

    def car_cast(self):
        return 400*self.car 
    
    def driver_cast(self):
        if self.extra_car >= 1:
            cast = ( (18-6-8) + (self.extra_car-1)*(18-6-8) + (self.time - 8 - self.earlist_time) ) * 30
        else:
            cast = (self.time-8-self.earlist_time) * 30
        if cast > 0:
            return cast
        else :
            return 0

    def chose_direct(self,point_list,father_route):
        now_is = self.route[len(self.route)-1]
        point_map = [i for i in range(Static.HAS_CENTER,len(point_list))]
        point_list_map = [i for i in range(len(point_list))]
        leave = list(set(point_map) - set(father_route) - set(self.route))
        right = [0 for i in range(len(point_list))]
        fenmu = 0
##        print point_map
##        print '#############################'
##        print 'leave is'
##        print leave
##
##        for i in point_map:
##            cost = self.time_window(self.route[len(self.route)-1],i,point_list)
##            #print 'cost is:'
##            #print cost
##            if i in leave:
##                tao_ij = information[ self.route[len(self.route)-1] ][ i ]
##                #print 'self.route[len(self.route)-1] is :'
##                #print self.route[len(self.route)-1]
##                #print 'i is:'
##                #print i
##                qifa = self.qifa_func( self.route[len(self.route)-1] , i ,point_list)
##                for j in leave:
##                    tao_is = information[ self.route[len(self.route)-1] ][ j ]
##                    qifa_is = self.qifa_func( self.route[len(self.route)-1] , j,point_list )
##                    fenmu += self.tao_and_qifa(tao_is,qifa_is)
##                    #print 'fenmu is :'
##                    #print fenmu
##                print 'lala'
##                right[i] = self.tao_and_qifa(tao_ij,qifa) / fenmu
##
        for i in leave:
            cost = self.time_window(self.route[len(self.route)-1],i,point_list)
            tao_ij = information[ self.route[len(self.route)-1] ][ i ]
            qifa = self.qifa_func( self.route[len(self.route)-1] , i ,point_list)
            for j in leave:
                tao_is = information[ self.route[len(self.route)-1] ][ j ]
                qifa_is = self.qifa_func( self.route[len(self.route)-1] , j,point_list )
                fenmu += self.tao_and_qifa(tao_is,qifa_is)
            right[i] = self.tao_and_qifa(tao_ij,qifa) / fenmu
        
##        print "right is"
##        print right
        right_final = [i/sum(right) for i in right]
        dubo = random.random()
        dubo_now = right_final[0]
        i = Static.HAS_CENTER
#        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
#        print right_final
        print sum(right_final)
        print right_final
        while(i<len(right_final) and sum(right_final)):
            #print i
            dubo_now += right_final[i]
            if dubo_now>dubo :
                if i in father_route or i in self.route:
                    right_final[i-1] = 0
                    i = Static.HAS_CENTER
                    continue
                #self.route.append(i)
                #self.time = self.time + point_list[self.route[len(self.route)-1]].work_time + self.distance(self.route[len(self.route)-1]],i) / CAR_SPEED
                #self.weight += point_list[i].weight            
                return i
            else:

                i += 1
                
        i = len(right_final)
        return i


    def tao_and_qifa(self,tao,qifa):
        return pow(tao,Static.WEIGHT_FOR_INFO)*pow(qifa,Static.WEIGHT_FOR_QIFA)
        

    def qifa_func(self,point1,point2,point_list):
        
        #return 1 / (distance(point1,point2))
        #print 'dis is '
##        print 'p1: ',
##        print point1,
##        print '         p2: ',
##        print point2
       # print Static.distance(point1,point2,point_list)
        if point1==point2:
            return 0
        return 1 / (self.cost + Static.distance(point1,point2,point_list))


    def ant_cycle(self,i,j,point_list):
        information[i-1][j-1] += Static.Q / Static.distance(i,j,point_list)

    def go_home(self,point_list):
##        print 'self route is:  '
##        print self.route
        temp = list()
        i = self.route[len(self.route)-1]
##        print 'i is:  ' + str(i)
        home = dict();
        for j in range(Static.HAS_CENTER):
            home[j] = Static.distance(i,j,point_list)
            print 'j is:  '+ str(j)
        result = sorted(home.iteritems(),key=lambda a : a[1])
        #result = sorted(home,key=lambda a : a[1])
        sum_temp = sum(home.keys())
        sum_temp1 = 0
##        print 'sum type'
##        print type(sum_temp)
##        print 'result[]'
##        print result
        for j in result:
            temp.append(list(j))
##        print temp
        for j in range(Static.HAS_CENTER):
            temp[j][1] = sum_temp / temp[j][1]
            sum_temp1 += temp[j][1]
        for j in range(Static.HAS_CENTER):
            temp[j][1] = temp[j][1] / sum_temp1
        new_result = sorted(temp,key=lambda a:a[1])
##        print temp
        time = self.time + point_list[self.route[len(self.route)-1]].work_time + Static.distance(self.route[len(self.route)-1],point_list[new_result[0][0]].id,point_list) / Static.CAR_SPEED
        s = 0
        while(time>Static.LAST_TIME):
            new_result.pop(0)
            time = self.time + point_list[self.route[len(self.route)-1]].work_time + Static.distance(self.route[len(self.route)-1],point_list[new_result[0][0]]) / CAR_SPEED
            s += 1
            if s==5:
                new_result.append([-1,-1])
                break
        return new_result[0][0] 

##########################################################################################

point_list = list()

##p0 = Point(42.395,-8.344,0,0,6.0,18,0)
##
##point_list.append(p0)
##
##p1 = Point(-42.175,-14.554,0,0,6.0,18,1)
##
##point_list.append(p1)
##
##p2 = Point(16.034,40.726,0,0,6.0,18,2)
##
##point_list.append(p2)
##
##p3 = Point(-14.639,29.633,0,0,6.0,18,3)
##
##point_list.append(p3)
## 
##p4 = Point(16.049,-3.934,0,0,6.0,18,4)
##
##point_list.append(p4)
##
##p5 = Point(46.112,12.430,0,0,6.0,18,5)
##
##point_list.append(p5)
##
##p6 = Point(-92.700,-59.180,8,0.27,8.0,12.5,6)
##
##point_list.append(p6)
##
##p7 = Point(71.179,12.543,15,0.50,6.5,12.0,7)
##
##point_list.append(p7)
##
##p8 = Point(31.537,66.638,20,0.67,6.5,10.0,8)
##
##point_list.append(p8)
##
##p9 = Point(-4.694,25.537,7,0.23,7.5,16.5,9)
##
##point_list.append(p9)
##
##p10 = Point(-30.194,67.773,13,0.43,8.5,15.5,10)
##
##point_list.append(p10)
##
##p11 = Point(12.677,-57.471,6,0.20,7.5,16.5,11)
##
##point_list.append(p11)
##
##p12 = Point(-32.355,-20.966,5,0.17,8.5,13.5,12)
##
##point_list.append(p12)
##
##p13 = Point(19.910,48.975,1,0.03,7.5,16.5,13)
##
##point_list.append(p13)
##
##p14 = Point(13.202,-19.135,12,0.40,7.0,11.5,14)
##
##point_list.append(p14)
##
##p15 = Point(54.877,-41.168,18,0.60,8.5,13.5,15)
##
##point_list.append(p15)
##
##p16 = Point(15.063,-25.171,25,0.83,6.5,10.0,16)
##
##point_list.append(p16)
##
##p17 = Point(-50.598,-16.418,14,0.47,6.5,12.0,17)
##
##point_list.append(p17)
##
##p18 = Point(-29.730,17.078,18,0.60,8.5,13.5,18)
##
##point_list.append(p18)
##
##p19 = Point(17.542,1.575,13,0.43,7.5,16.5,19)
##
##point_list.append(p19)
##
##p20 = Point(11.127,77.216,6,0.20,6.5,9.5,20)
##
##point_list.append(p20)
##
##p21 = Point(33.752,71.259,14,0.47,8.0,10.0,21)
##
##point_list.append(p21)
##
##p22 = Point(-56.012,-10.394,10,0.33,6.5,9.5,22)
##
##point_list.append(p22)
##
##p23 = Point(57.874,-16.290,18,0.60,7.5,13.5,23)
##
##point_list.append(p23)
##
##p24 = Point(10.718,-18.787,8,0.27,7.0,11.0,24)
##
##point_list.append(p24)
##
##p25 = Point(53.088,-18.750,6,0.20,8.5,11.5,25)
##
##point_list.append(p25)
##
##p26 = Point(1.569,7.532,2,0.07,6.5,10.0,26)
##
##point_list.append(p26)
##
##p27 = Point(31.531,48.944,4,0.13,7.0,9.5,27)
##
##point_list.append(p27)
##
##p28 = Point(-66.833,-37.854,4,0.13,8.5,15.5,28)
##
##point_list.append(p28)
##
##p29 = Point(-70.740,62.244,23,0.77,8.5,16.5,29)
##
##point_list.append(p29)
##
##p30 = Point(32.538,23.096,12,0.40,6.5,12.0,30)
##
##point_list.append(p30)
##
##p31 = Point(-51.453,-36.444,24,0.80,6.0,12.0,31)
##
##point_list.append(p31)
##
##p32 = Point(36.456,-22.638,17,0.57,6.5,9.5,32)
##
##point_list.append(p32)
##
##p33 = Point(-31.207,43.494,18,0.60,8.5,12.0,33)
##
##point_list.append(p33)
##
##p34 = Point(-10.388,34.491,25,0.83,7.5,15.5,34)
##
##point_list.append(p34)
##
##p35 = Point(14.722,-10.834,22,0.73,6.0,16.5,35)
##
##point_list.append(p35)
##
##p36 = Point(47.095,-21.387,10,0.33,7.0,14.5,36)
##
##point_list.append(p36)
##
##p37 = Point(43.781,34.766,25,0.83,8.5,13.5,37)
##
##point_list.append(p37)
##
##p38 = Point(53.546,-67.487,21,0.70,7.0,13.0,38)
##
##point_list.append(p38)
##
##p39 = Point(26.801,46.515,21,0.70,6.5,12.0,39)
##
##point_list.append(p39)
##
##p40 = Point(63.385,11.981,16,0.53,7.5,15.5,40)
##
##point_list.append(p40)
##
##p41 = Point(47.192,-5.475,23,0.77,6.5,10.5,41)
##
##point_list.append(p41)
##
##p42 = Point(-16.315,-11.267,21,0.70,8.5,16.0,42)
##
##point_list.append(p42)
##
##p43 = Point(78.900,17.651,15,0.50,7.5,12.0,43)
##
##point_list.append(p43)
##
##p44 = Point(79.822,22.272,7,0.23,6.0,16.5,44)
##
##point_list.append(p44)
##
##p45 = Point(12.878,16.919,20,0.67,7.5,11.5,45)
##
##point_list.append(p45)
##
##p46 = Point(-67.981,-3.754,6,0.20,6.0,10.0,46)
##
##point_list.append(p46)
##
##p47 = Point(9.198,-18.597,16,0.53,7.0,9.5,47)
##
##point_list.append(p47)
##
##p48 = Point(-35.950,-19.141,10,0.33,7.0,10.5,48)
##
##point_list.append(p48)
##
##p49 = Point(28.766,45.276,7,0.23,8.5,16.5,49)
##
##point_list.append(p49)
##
##p50 = Point(11.469,68.231,20,0.67,7.5,15.5,50)
##
##point_list.append(p50)
##
##p51 = Point(-22.760,45.496,9,0.30,6.5,16.5,51)
##
##point_list.append(p51)
##
##p52 = Point(-65.674,-23.120,12,0.40,7.0,14.5,52)
##
##point_list.append(p52)
##
##p53 = Point(7.239,1.599,10,0.33,8.5,13.5,53)
##
##point_list.append(p53)
##
##p54 = Point(-29.785,-11.285,19,0.63,8.5,12.0,54)
##
##point_list.append(p54)
##
##p55 = Point(-89.050,16.211,6,0.20,6.5,15.5,55)
##
##point_list.append(p55)
##
##p56 = Point(-46.887,-3.363,14,0.47,7.0,13.5,56)
##
##point_list.append(p56)
##
##p57 = Point(-14.972,30.621,23,0.77,6.5,13.5,57)
##
##point_list.append(p57)
##
##p58 = Point(-17.035,49.774,8,0.27,7.5,11.5,58)
##
##point_list.append(p58)
##
##p59 = Point(31.635,53.619,10,0.33,6.5,11.5,59)
##
##point_list.append(p59)
##
##p60 = Point(-3.577,13.342,14,0.47,8.5,13.5,60)
##
##point_list.append(p60)
##
##p61 = Point(33.008,58.960,3,0.10,6.5,10.0,61)
##
##point_list.append(p61)
##
##p62 = Point(-92.950,63.263,25,0.83,6.0,12.0,62)
##
##point_list.append(p62)
##
##p63 = Point(-9.137,-22.931,21,0.70,6.5,10.5,63)
##
##point_list.append(p63)
##
##p64 = Point(-39.960,6.195,5,0.17,8.5,15.5,64)
##
##point_list.append(p64)
##
##p65 = Point(28.430,-19.214,2,0.07,7.5,10.5,65)
##
##point_list.append(p65)
##
##p66 = Point(-28.540,-3.485,3,0.10,6.0,12.0,66)
##
##point_list.append(p66)
##
##p67 = Point(31.415,36.859,21,0.70,6.0,12.0,67)
##
##point_list.append(p67)
##
##p68 = Point(-49.426,60.602,1,0.03,7.0,9.5,68)
##
##point_list.append(p68)
##
##p69 = Point(-72.827,-27.765,25,0.83,7.0,15.5,69)
##
##point_list.append(p69)
##
##p70 = Point(60.083,-45.905,21,0.70,8.5,16.5,70)
##
##point_list.append(p70)
##
##p71 = Point(10.870,-3.900,21,0.70,7.5,13.0,71)
##
##point_list.append(p71)
##
##p72 = Point(25.122,7.672,25,0.83,8.5,15.5,72)
##
##point_list.append(p72)
##
##p73 = Point(-46.997,-17.474,14,0.47,6.5,16.5,73)
##
##point_list.append(p73)
##
##p74 = Point(16.058,33.020,20,0.67,6.0,13.5,74)
##
##point_list.append(p74)
##
##p75 = Point(25.409,-11.700,14,0.47,8.0,16.0,75)
##
##point_list.append(p75)
##
##p76 = Point(68.323,-5.145,11,0.37,8.5,12.0,76)
##
##point_list.append(p76)
##
##p77 = Point(-13.104,62.158,25,0.83,6.5,16.5,77)
##
##point_list.append(p77)

p0 = Point(42.395,-8.344,0,0,6.0,18,0)

point_list.append(p0)

p1 = Point(-42.175,-14.554,0,0,6.0,18,1)

point_list.append(p1)

p2 = Point(16.034,40.726,0,0,6.0,18,2)

point_list.append(p2)

p3 = Point(-14.639,29.633,0,0,6.0,18,3)

point_list.append(p3)
 
p4 = Point(16.049,-3.934,0,0,6.0,18,4)

point_list.append(p4)

p5 = Point(46.112,12.430,0,0,6.0,18,5)

point_list.append(p5)

p6 = Point(-92.700,-59.180,8,0.27,8.0,12.5,6)

point_list.append(p6)

p7 = Point(71.179,12.543,15,0.50,6.5,12.0,7)

point_list.append(p7)

p8 = Point(31.537,66.638,20,0.67,6.5,10.0,8)

point_list.append(p8)

print 'start'
Static.POINT_NUMBER = len(point_list)
information = [[1 for i in range(Static.POINT_NUMBER)] for j in range(Static.POINT_NUMBER)]
i = 0
while(i<Static.POINT_NUMBER):
    information[i][i] = 0
    i += 1
a = Ant_Colony()
a.lets_crazy(point_list)

print 'done'
