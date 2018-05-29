import numpy as np
from firebase import firebase
import json
from pprint import pprint
#import matplotlib.pyplot as plt
#import matplotlib.font_manager
#from sklearn import svm
#from least_squares_sine import sin_estimation

def initDataBase():
    with open(r'app/google-services.json') as f:
        data = json.load(f)

    pprint(data['project_info']['firebase_url'])

    fb = firebase.FirebaseApplication(data['project_info']['firebase_url'], None)
    #result = firebase.get('/Roee', None)
    return fb
    

class emp(object):
    '''
    This class holds the employee atributes
    '''
    def __init__(self,ID,name,title,slaryIndx,avgJobDuration,avgJobIncome):
        '''
        Employee atributes
        '''
        self.ID = ID
        self.name = name
        self.title = title
        self.slaryIndx = slaryIndx
        self.avgJobDuration=avgJobDuration
        self.avgJobIncome=avgJobIncome
        # App estimation:
        self.est_pBus=0.33
        self.est_pTaxi=0.33
        self.est_pWalk=0.34
        # Simulative truth (physical):
    
    def setEmpPref(self,pBus,pTaxi,pWalk):
        self.sim_pBus=pBus
        self.sim_pTaxi=pTaxi
        self.sim_pWalk=pWalk
        
        
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
    def __init__(self,name,price,duration,dist):
        self.name=name
        self.price=price
        self.duration=duration
        self.dist=dist
        

def calcTtlInc(employee,avlblTrns):
    print('')
    print('employee name:' + employee.name + ', title: ' + employee.title + ', slry: ' + str(employee.slaryIndx))
    print('avgJobDuration:' + str(employee.avgJobDuration) + ', avgJobIncome: ' + str(employee.avgJobIncome))
    ttlJobInc={'taxi':None, 'bus':None, 'walk':None}
    for tr in avlblTrns:
        print('\t*transport: ' + tr.name + ', price: ' + str(tr.price) + ', duration: ' + str(tr.duration) + ', dist: ' + str(tr.dist))
        ttlCommCost=tr.price+tr.duration*employee.slaryIndx
        print('\t total comm. cost: ' + str(ttlCommCost))
        #ttlDuration=employee.avgJobDuration+tr.duration
        print('\t Net Income Per Job:' + str(employee.avgJobIncome-ttlCommCost))
        ttlJobInc[tr.name]=employee.avgJobIncome-ttlCommCost
    return ttlJobInc
        
def fb2Trns(trnsDict):
    '''This function parses the firebase transpotation data into a 
    transport class.
    '''
    trnsList=[]
    for itm in trnsDict.keys():
        atribDict = trnsDict[itm]
        priceStr=atribDict['price']
        if ''==priceStr:
            continue
        else:
            low=float(priceStr.split(' ')[0])
            high=float(priceStr.split(' ')[2])
            price=0.5*(high+low)
            duration=float(atribDict['time'].split(':')[0])/60
            trnsList.append(transport(itm,price,duration,None))
    return trnsList

def simGetCommutes():
    trns=[]
    D=0.2+np.random.rand()*8 # randome range
    trns.append(transport('taxi',7+D*5,0.05+D/50,D)) #7 shkl + 5 shekel per km, 40Km/hour, 3min wait
    trns.append(transport('bus',5,0.16+D/15,D)) #5 sekel total, 15Km/hour, 10 min wait
    trns.append(transport('walk',0,D/6,D))
    return trns

''' USAGE:
#import the package:    
import get2work as g2w

#### create employees:
emps=[g2w.emp(12,'Roee','sales',25,0.5,100), g2w.emp(12,'guy','sales',45,0.4,125)]
# set employees transport preferences:
emps[0].setEmpPref(pBus=0.2,pTaxi=0.6,pWalk=0.2)
emps[1].setEmpPref(pBus=0.3,pTaxi=0.5,pWalk=0.2)


### From firebase:
# initiate firebase connection:
fb=g2w.initDataBase()

resRoee=fb.get('/Roee', None)
resGuy=fb.get('/guy', None)

import time
while True:
    for e in emps:
        # retrieve attributes of available commutes:
        fbRes=fb.get('/' + e.name, None)
        if True: #TODO: replace by 'needs an offer\incentive'
            avlblTrns=g2w.fb2Trns(fbRes)
            g2w.calcTtlInc(e,avlblTrns)
    time.sleep(4) # pause 4 sec


### From simulation:
import time
while True:
    fbRes=g2w.simGetCommutes()
    for e in emps:
        # retrieve attributes of available commutes:
        if True: #TODO: replace by 'needs an offer\incentive'
            avlblTrns=fbRes
            ttlInc=g2w.calcTtlInc(e,avlblTrns)
    time.sleep(4) # pause 4 sec

'''