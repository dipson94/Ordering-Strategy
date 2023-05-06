import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from math import sqrt
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from tabulate import tabulate
import warnings
number_of_replenishments=[]
warnings.filterwarnings('ignore')
n = int(input("\nenter sample size : "))
mean = int(input("enter mean : "))
deviation_percent = float(input("Enter % deviation : "))
replenishment=int(input("enter the size of replenishment : "))
std = int(mean * (deviation_percent / 100))
L=[int(input("enter Lead time 1 : "))]
L.append(int(input("enter Lead time 2 : ")))
alpha=[float(input("enter % service rate 1 : "))/100]
alpha.append(float(input("enter % service rate 2 : "))/100)
print("\n")
zalpha=[norm.ppf(alpha[0])]
zalpha.append(norm.ppf(alpha[1]))
sqrtL=[sqrt(L[0])]
sqrtL.append(sqrt(L[1]))
safety_stock=[]
reorder_point=[]
Demand=[]
initial_stock=[[0 for _ in range(0,n)] for _ in range(0,4)]
final_stock=[[0 for _ in range(0,n)] for _ in range(0,4)]
day=[x for x in range(1,n+1)]
order_size=[[0 for _ in range(0,n)] for _ in range(0,4)]
maximum_inventory=[]
for i in range(0,2):
    for j in range(0,2):
        safety_stock.append(zalpha[j]*sqrtL[i]*std)
        reorder_point.append((sqrtL[i]*sqrtL[i]*mean)+safety_stock[-1])

def random_nums(n,mean,std):  
    i=0
    x=[]
    while i<int(n/2):
        temp=2*mean
        while temp>(mean+std) or temp<(mean-std):
            temp=np.random.normal(mean,std)
        x.append(int(temp))
        i=i+1        
        
    y=[]

    for i in range(0,int(n/2)):
        
        if x[i]<mean:
            y.append((mean-x[i])+mean)
            
        elif x[i]>mean:
            y.append(mean-(x[i]-mean))
        else:
            y.append(x[i])
        y.append(x[i])
    nums=np.array(y)
    np.random.shuffle(nums)
    
    return [int(x) for x in nums]

for x in range (0,4):
    Demand.append(random_nums(int(n),int(mean),int(std)))
    initial_stock[x][0]=int(replenishment)
    number=0
    for i in range(0,n):
        final_stock[x][i]=int(initial_stock[x][i]-Demand[x][i])
        if (final_stock[x][i]<reorder_point[x] or final_stock[x][i]==reorder_point[x]) and i!=n-1:
            initial_stock[x][i+1]=int(final_stock[x][i]+replenishment)
            order_size[x][i]=int(replenishment)
            number=number+1
        elif i!=n-1:
            initial_stock[x][i+1]=int(final_stock[x][i])
    number_of_replenishments.append(number)
    maximum_inventory.append(np.max(initial_stock[x]))
result=[[0 for _ in range(0,8)] for _ in range(0,4)]
for i in range(0,4):
    if i%2==0:
        result[i][0]="{:.3f}".format(alpha[0])
        result[i][1]="{:.3f}".format(zalpha[0])
    else:
        result[i][0]="{:.3f}".format(alpha[1])
        result[i][1]="{:.3f}".format(zalpha[1])   
    if i<2:
        result[i][2]=L[0]
        result[i][3]="{:.2f}".format(sqrtL[0])
    else:
        result[i][2]=L[1]
        result[i][3]="{:.2f}".format(sqrtL[1])
    result[i][4]=int(safety_stock[i])
    result[i][5]=int(reorder_point[i])
    result[i][6]=int(np.max(initial_stock[i]))
    result[i][7]=int(number_of_replenishments[i])

results=pd.DataFrame(result,columns=["α","Zα","L","√L","Safety Stock","Reorder Point","Maximum Inventory","Times of replenishments"])
cx=np.stack((day,initial_stock[0],np.array(Demand[0]),final_stock[0],order_size[0]),axis=1)
c1=pd.DataFrame(np.stack((day,initial_stock[0],np.array(Demand[0]),final_stock[0],order_size[0]),axis=1),index=None,columns=["Day","Initial stock","Demand","Final Stock","Order size"])
c2=pd.DataFrame(np.stack((day,initial_stock[1],np.array(Demand[1]),final_stock[1],order_size[1]),axis=1),index=None,columns=["Day","Initial stock","Demand","Final Stock","Order size"])
c3=pd.DataFrame(np.stack((day,initial_stock[2],np.array(Demand[2]),final_stock[2],order_size[2]),axis=1),index=None,columns=["Day","Initial stock","Demand","Final Stock","Order size"])
c4=pd.DataFrame(np.stack((day,initial_stock[3],np.array(Demand[3]),final_stock[3],order_size[3]),axis=1),index=None,columns=["Day","Initial stock","Demand","Final Stock","Order size"])
writer = pd.ExcelWriter('Order.xlsx', engine='openpyxl')
workbook = writer.book
df=[results,pd.merge(c1, c2, on='Day').merge(c3, on='Day').merge(c4, on='Day')]
if "Order_Strategy" not in workbook.sheetnames:
    workbook.create_sheet("Order_Strategy")
if "Conditions" not in workbook.sheetnames:
    workbook.create_sheet("Conditions")    
sheets=["Order_Strategy","Conditions"]
for i in range(0,2):
    worksheet=workbook[sheets[i]]
    for row in worksheet.iter_rows():
        for cell in row:
            cell.value = None 
    df[i].to_excel(writer, sheet_name=sheets[i], startrow=0, startcol=0, header=True, index=False)
    writer.save()

print("\nResults ..........\n")
print(tabulate(results.values.tolist(), headers=results.columns, tablefmt='grid',stralign='left'))


print("\n\n\nCondition 1 ..........\t\t\t\t\t\tCondition 2 ..........\n")
print(tabulate(pd.merge(c1, c2, on='Day').values.tolist(), headers=pd.merge(c1, c2, on='Day').columns, tablefmt='grid',stralign='left'))
print("\n\n\nCondition 2 ..........\t\t\t\t\t\tCondition 3 ..........\n")
print(tabulate(pd.merge(c3, c4, on='Day').values.tolist(), headers=pd.merge(c3, c4, on='Day').columns, tablefmt='grid',stralign='left'))

plt.hist(Demand[0],bins=n,label='Condition 1')
plt.hist(Demand[1],bins=n,label='Condition 2')
plt.hist(Demand[2],bins=n,label='Condition 3')
plt.hist(Demand[3],bins=n,label='Condition 4')
plt.legend()
plt.savefig('distribution.png')
plt.show()
