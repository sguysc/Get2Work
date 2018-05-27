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
        #self.profit=profit
        
        
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
        self.duration=duration
        
        
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
        self.trns=[]
        D=np.abs(self.jobLocation-empLocation)
        self.trns.append(transport('taxi1',7+D*5,0.05+D/50)) #7 shkl + 5 shekel per km, 40Km/hour, 3min wait
        self.trns.append(transport('bus1',5,0.16+D/15)) #5 sekel total, 15Km/hour, 10 min wait
        self.trns.append(transport('bike',0,D/10))
        #self.trns.append(transport('walk',0,D/4))
        

def calcOffers(agenda,employee,jobAndAcc,empLoc):
    # update jobAndAccess attribs for employee location:
    jobAndAcc.getCommuteOptions(empLoc)
    print('employee name:' + employee.name + ', title: ' + employee.title + ', slry: ' + str(employee.slaryIndx))
    print('Job distance: abs(' + str(jobAndAcc.jobLocation) + '-' + str(empLoc) + ')=' + str(np.abs(empLoc-jobAndAcc.jobLocation)) + 'Km')
    print('job transportation options:')
    for tr in jobAndAcc.trns:
        print('\ttransport: ' + tr.name + ', price: ' + str(tr.price) + ', duration: ' + str(tr.duration))
        print('\ttotal cost: ' + str(tr.price+tr.duration*employee.slaryIndx))
        
    


''' USAGE:
    
import get2work as g2w

# create employees:
sam=g2w.emp(12,'sam','sales',35)
rob=g2w.emp(12,'rob','sales',45)

#create a job:
j1=g2w.jobAndAccess(6) # job location==6km
j2=g2w.jobAndAccess(2.5) # job location==2.5km


# set company agenda:
A1=g2w.cmpnyGreenAgenda('greedy',0.2)
A2=g2w.cmpnyGreenAgenda('greeny',0.7)

# set employee location:
empLoc=1 #employee location == -3Km

# calculate offers:
g2w.calcOffers(A1,sam,j1,empLoc)
g2w.calcOffers(A1,rob,j1,empLoc)
g2w.calcOffers(A1,sam,j2,empLoc)
g2w.calcOffers(A1,rob,j2,empLoc)

    
'''