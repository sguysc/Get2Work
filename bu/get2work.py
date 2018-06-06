import numpy as np
from firebase import firebase
import json
from pprint import pprint
from sklearn import svm
#import matplotlib.pyplot as plt
#import matplotlib.font_manager
#from sklearn import svm
#from least_squares_sine import sin_estimation

def initDataBase():
    '''
    Load the project database using firebase.
    '''
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
        self.svm2trns_data={'bike': [[[-1],[100]],[0,1]],
                            'bus': [[[-1],[100]],[0,1]],
                            'walk': [[[-1],[100]],[0,1]]}
        self.svmNumElems=20
        self.prefReal={'taxi':None,'bus':None,'bike':None,'walk':None}
        # Simulative truth (physical):
        self.cmpnyAg=cmpnyGreenAgenda()
        self.clf = svm.SVC(kernel='linear')
    
    
    def setEmpPref(self,pBus,pTaxi,pBike,pWalk):
        '''
        setEmpPref - sets employee preferences. Used solely in simulation mode.
        prefReal['XXX'] - the probability of choosing transport XXX (in case of equal promotions per transport)
        '''
        totSum=pBus+pTaxi+pBike+pWalk
        self.prefReal['bus']=pBus/totSum
        self.prefReal['taxi']=pTaxi/totSum
        self.prefReal['bike']=pBike/totSum
        self.prefReal['walk']=pWalk/totSum
        
        
    def estIncentiveSVM(self,trnsType):
        '''
        estIncentiveSVM - calculates the svm decision threshhold\plane for predicting the minimal amount of
        promotion\incentive inorder to "convince" the employee (self) to choose a transport of type "trnsType".
        This is done based on history of promotions-choices stored in employee.svm2trns_data.
        '''
        trnDat=self.svm2trns_data[trnsType]
        L=len(trnDat[1])
        wght=list(np.exp(-np.array(range(L-1,-1,-1))/L))
        self.clf.fit(trnDat[0],trnDat[1],sample_weight= wght )
        decPlane=np.mean(self.clf.support_vectors_)
        return decPlane
        #clf.predict(dNew)

class cmpnyGreenAgenda(object):
    '''
    This class is a company agenda towards promoting green choices and saving money.
    '''
    def __init__(self):
        self.name=None
        self.leaf2money=1
        # geenIndex - an arbitrary order of the trans options
        self.geenIndex=['walk','bike','bus','taxi']
        # geenAgenda - the company choice of "greenest" transportation type to least.
        self.geenAgenda=['walk','bike','bus','taxi']
    
    def changeAgenda(self,newOrdr):
        for i in range(newOrdr):
            self.geenAgenda[i]=self.geenIndex[newOrdr[i]]
        

class transport(object):
    '''
    Class for storing transportation attributes.
    '''
    def __init__(self,name,price,duration,dist):
        self.name=name
        self.price=price
        self.duration=duration
        self.dist=dist
        

def calcTtlInc(employee,avlblTrns):
    '''
    Calculates totla income with respect to different transportation types
    '''
    #print('')
    #print('employee name:' + employee.name + ', title: ' + employee.title + ', slry: ' + str(employee.slaryIndx))
    #print('avgJobDuration:' + str(employee.avgJobDuration) + ', avgJobIncome: ' + str(employee.avgJobIncome))
    ttlJobInc={'taxi':None, 'bus':None, 'walk':None, 'bike':None}
    for tr in avlblTrns:
        #print('\t*transport: ' + tr.name + ', price: ' + str(tr.price) + ', duration: ' + str(tr.duration) + ', dist: ' + str(tr.dist))
        ttlCommCost=tr.price+tr.duration*employee.slaryIndx
        #print('\t total comm. cost: ' + str(ttlCommCost))
        #ttlDuration=employee.avgJobDuration+tr.duration
        #print('\t Net Income Per Job:' + str(employee.avgJobIncome-ttlCommCost))
        ttlJobInc[tr.name]=employee.avgJobIncome-ttlCommCost
    return ttlJobInc
        
def fb2Trns(trnsDict):
    '''
    This function parses the input from firebase transpotation data into a 
    transport class.
    '''
    trnsList=[]
    for itm in trnsDict.keys():
        atribDict = trnsDict[itm]
        priceStr=atribDict['price']
        if ''==priceStr:
            continue
        else:
            if priceStr.count(' ')<=1:
                price=float(priceStr.split(' ')[0])
            else:
                low=float(priceStr.split(' ')[0])
                high=float(priceStr.split(' ')[2])
                price=0.5*(high+low)
            duration=float(atribDict['time'].split(':')[0])/60
            trnsList.append(transport(itm,price,duration,None))
    return trnsList

def simGetCommutes():
    '''
    This function simulatively generates all transport type to a destination.
    Used only in simulation mode.
    '''
    trns=[]
    D=0.2+np.random.rand()*8 # randome range
    trns.append(transport('taxi',7+D*5,0.05+D/50,D)) #7 shkl + 5 shekel per km, 40Km/hour, 3min wait
    trns.append(transport('bus',5,0.16+D/15,D)) #5 sekel total, 15Km/hour, 10 min wait
    trns.append(transport('bike',5,0.05+D/8,D))
    trns.append(transport('walk',0,D/6,D))
    return trns


''' USAGE:
#import the package:    
import get2work as g2w

#### create employees:
emps=[g2w.emp(12,'roee','sales',25,0.5,100), g2w.emp(12,'guy','sales',45,0.4,125)]
# set employees transport preferences:
emps[0].setEmpPref(pBus=0.2,pTaxi=0.6,pWalk=0.1,pBike=0.1)
emps[1].setEmpPref(pBus=0.3,pTaxi=0.5,pWalk=0.1,pBike=0.1)


### From firebase:
# initiate firebase connection:
fb=g2w.initDataBase()

resRoee=fb.get('/roee', None)
resGuy=fb.get('/guy', None)
resAmir=fb.get('/amir', None)
resAmihay=fb.get('/amihay',None)

import time
Flag1=True
while Flag1:
    for e in emps:
        # retrieve attributes of available commutes:
        fbRes=fb.get('/' + e.name, None)
        if True: #TODO: replace by 'needs an offer\incentive'
            avlblTrns=g2w.fb2Trns(fbRes)
            g2w.calcTtlInc(e,avlblTrns)
    Flag=False
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
            print(ttlInc)
    time.sleep(4) # pause 4 sec

'''