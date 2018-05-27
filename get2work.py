import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.font_manager
#from sklearn import svm
#from least_squares_sine import sin_estimation

class emp(object):
    '''
    This class holds the employee atributes
    '''
    def __init__(self,ID,name,title,slaryIndx):
        '''
        Employee atributes
        '''
        self.ID = ID
        self.name = name
        self.title = title
        self.slaryIndx = slaryIndx
        
        
    '''def setTitle(self,title):
        self.title=title
        
    def setSlaryIndx(self,slaryIndx):
        self.slaryIndx=slaryIndx'''


class cmpnyGreenAgenda(object):
    '''
    This class is a company agenda towards promoting green choices and saving money.
    '''
    def __init__(self,name,leaf2money):
        self.name=name
        self.leaf2money=leaf2money
        

class transport(object):
    def __init__(self,name,price,duration):
        self.name=name
        self.price=price
        self.duratioin=duration
        
        
class jobAndAccess(object):
    def __init__(self,jobLocation):
        '''
        for now, a location along x axis
        TODO: get real location object from DB
        '''
        self.jobLocation=jobLocation
        self.trns=[]
        
    def getCommuteOptions(self,empLocation):
        '''
        Input: empLocation - a location along x axis (for now)
        TODO: change input location to real location object
        TODO: query database via firebase for real time and prices for commutes
        '''
        D=np.abs(self.jobLocation-empLocation)
        self.trns.append(transport('taxi1',D*5,D/40)) #5 sekel per km, 40Km/hour
        self.trns.append(transport('bus1',5,D/15)) #5 sekel total, 15Km/hour
        self.trns.append(transport('bike',0,D/10))
        self.trns.append(transport('walk',0,D/4))
        

def calcOffers(agenda,employee,jobAndAcc,empLoc):
    


''' USAGE:
    
import get2work as g2w

# create employees:
sam=g2w.emp(12,'sam','sales',40)
rob=g2w.emp(12,'rob','sales',45)

#create a job:
j1=g2w.jobAndAccess(15) # job location==15km

# set company agenda:
A1=g2w.cmpnyGreenAgenda('greedy',0.2)
A2=g2w.cmpnyGreenAgenda('greeny',0.7)

# set employee location:
empLoc=-3 #employee location == -3Km
# update jobAndAccess attribs for employee location:
j1.getCommuteOptions(empLoc)

# calculate offers:
calcOffers(A1,sam,j1,empLoc)
    
'''