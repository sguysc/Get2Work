# -*- coding: utf-8 -*-
"""
get to work simulator

Created on Thu May 31 21:01:59 2018

@author: ROEE


"""
empbusOffer={'roee':[[],[],[]],'guy':[[],[],[]]}
savingsRoee={'maxSavings':[],'netSavings':[],'promotions':[]}
savingsGuy={'maxSavings':[],'netSavings':[],'promotions':[]}
import pdb

def getEmpOffer(Emp,netIncDict):
    import operator
    
    '''
    Checks if least "green" option is also the most profitable.
    If so, then no "win win win" option possible.
    '''
    leastGreenTrns=Emp.cmpnyAg.geenAgenda[-1]
    if max([x-netIncDict[leastGreenTrns] for x in netIncDict.values()])<=0.99:
        return None
    
    
    '''
    Calculate the profit of switching to a surtain transportation:
    TODO: for now this code assumes that 'taxi' is leas green. Switch to -> Emp.cmpnyAg.geenAgenda[-1]
    '''
    switchTo={'walk':max([netIncDict['walk']-netIncDict['taxi'],netIncDict['walk']-netIncDict['bus'],netIncDict['walk']-netIncDict['bike'],0]),
          'bike':max([netIncDict['bike']-netIncDict['taxi'],netIncDict['bike']-netIncDict['bus'],0]),
          'bus': max([netIncDict['bus']-netIncDict['taxi'],0])}
    sw2srt=[sorted(switchTo.items(),key=operator.itemgetter(1),reverse=True)[0]]    
    
    
    
    '''
    Remove non-green incentive options:
    
    If sw2str economical order is: 'Bus', 'Bike', 'Walk'.
    Then promote only 'Bus' since promoting 'Bike' might reduce 'Bus' promotion effect.
    
    e.g. :  If 'Bus' is most economic then dont promote 'Bike'.
            If 'Walk' is most economic then its ok to also promote 'Bike' (if its more economical than 'Bus'\'Taxi')
            Hope for order: Walk, Bike, Bus (or as in cmpnyAg.geenAgenda)
    
    nTypes=len(Emp.cmpnyAg.geenAgenda)
    prevGreenIndex=-1
    for itm, i in zip(sw2srt, range(len(sw2srt))):
        currGreenIndx=Emp.cmpnyAg.geenAgenda.index(itm[0])
        if currGreenIndx>prevGreenIndex and currGreenIndx<nTypes-1:
            prevGreenIndex=currGreenIndx
            continue
        else:
            prevGreenIndex=nTypes
            sw2srt[i]=(sw2srt[i][0],0)
    '''
    
    '''
    Calaulte insentive ammount for profitable options:
    offer only smaller incentives than of the most profitable one
    '''
    lastBen=10000
    for itm, i in zip(sw2srt, range(len(sw2srt))):
        nDat=len(Emp.svm2trns_data[itm[0]][1])
        if nDat>3:
            #pdb.set_trace()
            #if Emp.name=='Roee' and 'bus'==itm[0]:
            #    pdb.set_trace()
            #    print(Emp.svm2trns_data['bus'])
            decPlane = Emp.estIncentiveSVM(itm[0])
            est=max([min([decPlane+1*np.random.randn(),sw2srt[i][1],lastBen]),0])
            sw2srt[i]=(sw2srt[i][0],(sw2srt[i][1],est))
        elif nDat==3:
            sw2srt[i]=(sw2srt[i][0],(sw2srt[i][1],sw2srt[i][1]*0.1))
        elif nDat==2:
            sw2srt[i]=(sw2srt[i][0],(sw2srt[i][1],sw2srt[i][1]))
        lastBen=sw2srt[i][1][1]
    
    #pdb.set_trace()
    for trnsType in Emp.cmpnyAg.geenAgenda:
        if trnsType != sw2srt[0][0]:
            sw2srt.append((trnsType,(0,0)))
    print('Offer: ' + str(sw2srt))
    
    return sw2srt

def getEmpChoice(Emp,sw2srt):
    import operator
    
    #Calculate employees choice based on simulation modle \ or external input
    empRealExp=[(keyStr,(5+tpl[1])*Emp.prefReal[keyStr]+0*np.random.randn(),Emp.prefReal[keyStr]) for keyStr, tpl in sw2srt]
    #empRealExp.append(('taxi',0,Emp.prefReal['taxi']))
    
    empRealExp=sorted(empRealExp,key=operator.itemgetter(1,2),reverse=True)
    empRealChoiceStr=empRealExp[0][0]
    print('Emp real choice: ' + str(empRealExp))
    return empRealChoiceStr

def learnChoiceVsOffer(Emp,sw2srt,empRealChoiceStr):
    if SimMode:
        if 'bus'==sw2srt[0][0] and (Emp.name=='roee' or Emp.name=='guy'):
            empbusOffer[Emp.name][0].append(sw2srt[0][1][1])
            empbusOffer[Emp.name][1].append(empRealChoiceStr==sw2srt[0][0])
            #pdb.set_trace()
    
    nDat=len(Emp.svm2trns_data[sw2srt[0][0]][1])
    if Emp.svmNumElems==nDat:
        # if the history buffer is full, remove old examples.
        #pdb.set_trace()
        Emp.svm2trns_data[sw2srt[0][0]][0].pop(2)
        Emp.svm2trns_data[sw2srt[0][0]][1].pop(2)
        
    Emp.svm2trns_data[sw2srt[0][0]][0].append([sw2srt[0][1][1]])
    
    if empRealChoiceStr==sw2srt[0][0]: #Emp.cmpnyAg.geenAgenda.index(empRealChoiceStr)<=Emp.cmpnyAg.geenAgenda.index(sw2srt[0][0]):
        Emp.svm2trns_data[sw2srt[0][0]][1].append(1)
    else:
        Emp.svm2trns_data[sw2srt[0][0]][1].append(0)
                
    #indToLearnPos=Emp.cmpnyAg.geenAgenda.index(empRealChoiceStr)
    #indToLearnNeg=range(indToLearnPos+1,nTypes+1)
    print('Learn ' + Emp.name + ': \n' + str(Emp.svm2trns_data))
    #pdb.set_trace()
    return

def fbGetWrap(fb,pth,notUsed):
    '''
    This function is a wrapper for firebase get.
    Its should be used to reduce crashes due to connection failures.
    '''
    numFails=0
    Success=False
    import time
    while not Success:
        try:
            res = fb.get(pth,notUsed)
            Success=True
        except:
            numFails+=1
            time.sleep(2)
        if numFails>5:
            print('fb.get: Oh well, connection failure :-(')
            return []
    return res

def fbPutWrap(fb,pth,pthEnd,val):
    '''
    This function is a wrapper for firebase get.
    Its should be used to reduce crashes due to connection failures.
    '''
    if type(val)!=str:
        val=str(val)
    
    numFails=0
    Success=False
    import time
    while not Success:
        try:
            res = fb.put(pth, pthEnd, val)
            Success=True
        except:
            numFails+=1
            time.sleep(2)
        if numFails>5:
            print('fb.put: Oh well, connection failure :-(')
            return None

    return res

    
def plusOneGen():
    i=0
    while True:
        yield i
        i+=1


#import the get to work package:    
import get2work as g2w
import numpy as np

#Choose simulation True or False:
SimMode=False

#%% Make \ Obtain employees:
if SimMode:
    #### create employees:
    emps=[g2w.emp(12,'roee','sales',25,0.5,100),
          g2w.emp(12,'guy','sales',45,0.4,125),
          g2w.emp(12,'amihay','sales',30,0.5,90),
          g2w.emp(12,'amir','sales',45,0.4,250)]
    # set employees transport preferences:
    emps[0].setEmpPref(pBus=0.2,pTaxi=0.6,pWalk=0.1,pBike=0.1)
    emps[1].setEmpPref(pBus=0.3,pTaxi=0.5,pWalk=0.1,pBike=0.1)
    emps[2].setEmpPref(pBus=0.2,pTaxi=0.6,pWalk=0.1,pBike=0.1)
    emps[3].setEmpPref(pBus=0.3,pTaxi=0.5,pWalk=0.1,pBike=0.1)
else:
    # initiate firebase connection:
    emps=[]
    fb=g2w.initDataBase()
    aaa=fbGetWrap(fb,'/Here',None)
    for ind, empName in zip(range(len(aaa)),aaa.keys()):
        salary = np.random.randint(25,45)
        hoursPerClient=np.random.rand()
        netIncomeFromClient=60+200*np.random.rand()
        E=g2w.emp(ind,empName,'sales',salary,hoursPerClient,netIncomeFromClient)
        E.setEmpPref(pBus=np.random.rand(),
                     pTaxi=np.random.rand(),
                     pWalk=np.random.rand(),
                     pBike=np.random.rand())
        emps.append(E)
#%%
        
emptyOffer = [('walk', (0,0)), ('bus', (0,0)), ('bike', (0,0)), ('taxi', (0,0))]
import time


if SimMode:
    rng=range(200)
else:
    rng=plusOneGen()

for iii in rng:
    if SimMode:
        fbRes=g2w.simGetCommutes()
        avlblTrns=fbRes
        
    for e in emps:
        if not SimMode:
            #pdb.set_trace()
            fbRes=fbGetWrap(fb,'/Here/' + e.name + '/ride', None)
            try:
                usedList=sum([int(vv['used']) for vv in [v for v in list(fbRes.values())]])
            except:
                usedList=0
            numEmptyLeafs=sum([int(vv['leafs']=='') for vv in [v for v in list(fbRes.values())]])
            #print(e.name + " {}".format(numEmptyLeafs))
            if numEmptyLeafs == 4: #Needs an offer (promotion)
                print('')
                print('Employee: ' + e.name + ', promotion needed:')
                avlblTrns=g2w.fb2Trns(fbRes)
                ttlInc=g2w.calcTtlInc(e,avlblTrns)
                # calculate offer \ promotion based on ttlInc:
                sw2srt=getEmpOffer(e,ttlInc)
                if None == sw2srt:
                    #empty offer
                    for trnsTypesStr in e.cmpnyAg.geenIndex:
                        fbPutWrap(fb, '/Here/' + e.name + '/ride/' + trnsTypesStr, 'leafs', '0')
                        fbPutWrap(fb, '/Here/' + e.name + '/ride/' + trnsTypesStr, 'used', '1')
                else:
                    #set leafs:
                    guy = 0
                    for trnsType in sw2srt:
                        if(trnsType[1][1] > 0):
                            guy = trnsType[1][1] # was trnsType[1][0], fixed by roee on 6,6,18 @ 22:00
                            fbPutWrap(fb, '/Here/' + e.name + '/ride/' + trnsType[0], 'leafs', "%.0f" % trnsType[1][0])
                        else:
                            fbPutWrap(fb, '/Here/' + e.name + '/ride/' + trnsType[0], 'leafs', "%.0f" % (guy * np.random.rand(1)))
                        fbPutWrap(fb,'/Here/' + e.name + '/ride/' + trnsType[0], 'used', '1')
                        
            elif 4==usedList:
                # wait for input from user
                continue
            elif 1==usedList:
                # pdb.set_trace()
                # learn from choice:
                for k, val in fbRes.items():
                    if fbRes[k]['used']=='1':
                        empRealChoiceStr=k
                        break
                #recalculate offer:
                avlblTrns=g2w.fb2Trns(fbRes)
                ttlInc=g2w.calcTtlInc(e,avlblTrns)
                sw2srt=getEmpOffer(e,ttlInc)
                #learn from choice:
                learnChoiceVsOffer(e,sw2srt,empRealChoiceStr)
                fbPutWrap(fb,'/Here/' + e.name + '/ride/' + empRealChoiceStr, 'used', '0')
                continue
            
        else:
            ttlInc=g2w.calcTtlInc(e,avlblTrns)
            
            print('')
            print('Employee: ' + e.name + ':')
            # calculate total income VS transportation type:
            
            print('Total income:' + str(ttlInc))
            # calculate offer \ promotion based on ttlInc:
            sw2srt=getEmpOffer(e,ttlInc)
            if None == sw2srt:
                # No "win win win" option :-(
                empRealChoiceStr=getEmpChoice(e,emptyOffer)
            else:
                empRealChoiceStr=getEmpChoice(e,sw2srt)
                tmp=dict(sw2srt)
                if e.name=='roee':
                    savingsRoee['maxSavings'].append(tmp[empRealChoiceStr][0])
                    savingsRoee['netSavings'].append(tmp[empRealChoiceStr][0]-tmp[empRealChoiceStr][1])
                    savingsRoee['promotions'].append(tmp[empRealChoiceStr][1])
                elif e.name=='guy':
                    savingsGuy['maxSavings'].append(tmp[empRealChoiceStr][0])
                    savingsGuy['netSavings'].append(tmp[empRealChoiceStr][0]-tmp[empRealChoiceStr][1])
                    savingsGuy['promotions'].append(tmp[empRealChoiceStr][1])
                learnChoiceVsOffer(e,sw2srt,empRealChoiceStr)
    if not SimMode:        
        time.sleep(1) # pause 1 sec
        
        
        
from matplotlib import pyplot as plt
plt.plot(emps[2].svm2trns_data['bus'][0][2:])