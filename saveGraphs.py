# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 22:24:32 2018

@author: ROEE
"""
empName='guy'
L=len(empbusOffer[empName][0])
Mx=max(empbusOffer[empName][0])
Mn=min(empbusOffer[empName][0])
for i in range(L):
    for j in range(i+1):
        if empbusOffer[empName][1][j]:
            plt.plot(j,empbusOffer[empName][0][j],marker='o',color='b')
        else:
            plt.plot(j,empbusOffer[empName][0][j],marker='o',color='r')
    plt.plot(empbusOffer[empName][0][:(i+1)]);
    plt.title(empName + ' Bus Promotion Learn');
    plt.ylabel('leafs');
    plt.xlim(0,L+1);
    plt.ylim(Mn-1,Mx+1);
    #plt.savefig(fname=empName + 'Bus'+str(i),dpi=100);
    plt.show()
#%%
images = []

for i in range(L):
    images.append(imageio.imread(empName + 'Bus'+str(i) + '.png'))
    

imageio.mimsave(empName + 'BusLearn2.gif', images)
#%%
plt.plot(np.cumsum(savingsRoee['maxSavings']));
plt.plot(np.cumsum(savingsRoee['netSavings']));
plt.title('max savings , get2work savings');plt.ylabel('money');plt.xlabel('rides');
plt.savefig('Max possible savings',dpi=200)

#%%
plt.plot(np.cumsum(savingsRoee['promotions']));
plt.title('get2work promotions');plt.ylabel('money');plt.xlabel('rides');
plt.savefig('promotionks',dpi=200)

#%%
L=len(savingsRoee['maxSavings'])
x=range(0,L)
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.fill_between(x, np.cumsum(savingsRoee['netSavings']), np.cumsum(savingsRoee['maxSavings']))
ax1.fill_between(x, 0, np.cumsum(savingsRoee['netSavings']))
ax1.set_ylabel('savings')
ax2.fill_between(x, 0, np.cumsum(savingsRoee['promotions']))
ax2.set_ylabel('promotions')
