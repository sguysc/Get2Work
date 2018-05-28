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
        
        
#class jobAndAccess(object):
#    def __init__(self,jobLocation):
#        '''
#        for now, a location along x axis
#        TODO: get real location object from DB
#        '''
#        self.jobLocation=jobLocation
#        self.trns=[]
#        
#    def getCommuteOptions(self,empLocation):
#        '''
#        Input: empLocation - a location along x axis (for now)
#        TODO: change input location to real location object
#        TODO: query database via firebase for real time and prices for commutes
#        '''
#        self.trns=[]
#        D=np.abs(self.jobLocation-empLocation)
#        self.trns.append(transport('taxi1',7+D*5,0.05+D/50)) #7 shkl + 5 shekel per km, 40Km/hour, 3min wait
#        self.trns.append(transport('bus1',5,0.16+D/15)) #5 sekel total, 15Km/hour, 10 min wait
#        self.trns.append(transport('bike',0,D/10))
#        #self.trns.append(transport('walk',0,D/4))
        

def calcOffers(employee,avlblTrns):
    print('employee name:' + employee.name + ', title: ' + employee.title + ', slry: ' + str(employee.slaryIndx))
    for tr in avlblTrns:
        print('\ttransport: ' + tr.name + ', price: ' + str(tr.price) + ', duration: ' + str(tr.duration))
        print('\ttotal cost: ' + str(tr.price+tr.duration*employee.slaryIndx))
        
def fb2Trns(trnsDict):
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
            trnsList.append(transport(itm,price,duration))
    return trnsList
        

''' USAGE:
#import the package:    
import get2work as g2w

# initiate firebase connection:
fb=g2w.initDataBase()

resRoee=fb.get('/Roee', None)
resGuy=fb.get('/guy', None)

# create employees:
emps=[g2w.emp(12,'Roee','sales',35), g2w.emp(12,'guy','sales',45)]


import time
while True:
    for e in emps:
        # retrieve attributes of available commutes:
        fbRes=fb.get('/' + e.name, None)
        if True: #TODO: replace by 'needs an offer\incentive'
            avlblTrns=g2w.fb2Trns(fbRes)
            g2w.calcOffers(e,avlblTrns)
    time.sleep(4) # pause 4 sec
    
'''