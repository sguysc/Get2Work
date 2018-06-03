# -*- coding: utf-8 -*-
"""
get to work simulator

Created on Thu May 31 21:01:59 2018

@author: ROEE


"""
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
            est=max([min([decPlane,sw2srt[i][1],lastBen]),0])
            sw2srt[i]=(sw2srt[i][0],(sw2srt[i][1],est))
        elif nDat==2:
            sw2srt[i]=(sw2srt[i][0],(sw2srt[i][1],0))
        elif nDat==3:
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
    empRealExp=[(keyStr,tpl[1]*Emp.prefReal[keyStr],Emp.prefReal[keyStr]) for keyStr, tpl in sw2srt]
    #empRealExp.append(('taxi',0,Emp.prefReal['taxi']))
    empRealExp=sorted(empRealExp,key=operator.itemgetter(1,2),reverse=True)
    empRealChoiceStr=empRealExp[0][0]
    print('Emp real choice: ' + str(empRealExp))
    return empRealChoiceStr

def learnChoiceVsOffer(Emp,sw2srt,empRealChoiceStr):
    #if 'bus'==sw2srt[0][0] and Emp.name=='Roee':
    #    pdb.set_trace()
        
    nDat=len(Emp.svm2trns_data[sw2srt[0][0]][1])
    if Emp.svmNumElems==nDat:
        # if the history buffer is full, remove old examples.
        #pdb.set_trace()
        Emp.svm2trns_data[sw2srt[0][0]][0].pop(2)
        Emp.svm2trns_data[sw2srt[0][0]][1].pop(2)
        
    Emp.svm2trns_data[sw2srt[0][0]][0].append([sw2srt[0][1][1]])
    
    if Emp.cmpnyAg.geenAgenda.index(empRealChoiceStr)<=Emp.cmpnyAg.geenAgenda.index(sw2srt[0][0]):
        Emp.svm2trns_data[sw2srt[0][0]][1].append(1)
    else:
        Emp.svm2trns_data[sw2srt[0][0]][1].append(0)
                
    #indToLearnPos=Emp.cmpnyAg.geenAgenda.index(empRealChoiceStr)
    #indToLearnNeg=range(indToLearnPos+1,nTypes+1)
    print('Learn ' + Emp.name + ': \n' + str(Emp.svm2trns_data))
    #pdb.set_trace()
    return
    

    
#import the package:    
import get2work as g2w

#### create employees:
emps=[g2w.emp(12,'roee','sales',25,0.5,100), g2w.emp(12,'guy','sales',45,0.4,125),
      g2w.emp(12,'amihay','sales',30,0.5,90), g2w.emp(12,'amir','sales',45,0.4,250)]


SimMode=True

if SimMode:
    # set employees transport preferences:
    emps[0].setEmpPref(pBus=0.2,pTaxi=0.6,pWalk=0.1,pBike=0.1)
    emps[1].setEmpPref(pBus=0.3,pTaxi=0.5,pWalk=0.1,pBike=0.1)
    emps[2].setEmpPref(pBus=0.2,pTaxi=0.6,pWalk=0.1,pBike=0.1)
    emps[3].setEmpPref(pBus=0.3,pTaxi=0.5,pWalk=0.1,pBike=0.1)
else:
    # initiate firebase connection:
    fb=g2w.initDataBase()

emptyOffer = [('walk', (0,0)), ('bus', (0,0)), ('bike', (0,0)), ('taxi', (0,0))]
import time
#TODO: change to while true instead of for loop
for iii in range(15):
    if SimMode:
        fbRes=g2w.simGetCommutes()
        avlblTrns=fbRes
        
    for e in emps:
        if not SimMode:
            fbRes=fb.get('/' + e.name, None)
            if True: #TODO: replace by 'needs an offer'
                avlblTrns=g2w.fb2Trns(fbRes)
                g2w.calcTtlInc(e,avlblTrns)
            else:
                # if doesnt need ride, then go to next employee
                continue
            
        print('')
        print('Employee: ' + e.name + ':')
        # calculate total income VS transportation type:
        ttlInc=g2w.calcTtlInc(e,avlblTrns)
        print('Total income:' + str(ttlInc))
        # calculate offer \ promotion based on ttlInc:
        sw2srt=getEmpOffer(e,ttlInc)
        if None == sw2srt:
            # No "win win win" option :-(
            empRealChoiceStr=getEmpChoice(e,emptyOffer)
        else:
            empRealChoiceStr=getEmpChoice(e,sw2srt)
            learnChoiceVsOffer(e,sw2srt,empRealChoiceStr)
    if not SimMode:        
        time.sleep(4) # pause 4 sec