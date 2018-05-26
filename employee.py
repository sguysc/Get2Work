#import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.font_manager
#from sklearn import svm
#from least_squares_sine import sin_estimation

#employee:
class employee(object):
    '''
    This class maintains the employee object
    '''
    Nemps=0
    IDs=[]
    def __init__(self,ID,name,title):
        '''
        Employee atributes
        '''
        self.ID = ID
        self.name = name
        self.title = title
        self.slaryIndx = None
        self.state = 'idle'
        self.greenIndx = None
        self.Nemps+=1
        self.IDs.append(ID)
        
    def setTitle(self,title):
        self.title=title
        
    def setSlaryIndx(self,slaryIndx):
        self.slaryIndx=slaryIndx

    def setState(self,state):
        self.state=state
        
    def setGreenIndx(self,greenIndx):
        self.greenIndx=greenIndx
    
    def remEmp(self,ID):
        if ID in self.IDs:
            self.IDs.remove(ID)
            self.Nemps-=1
        



#if __name__ == __main__:
#    elAp.addTrainData
