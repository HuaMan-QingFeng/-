# 1. 请以课程1成绩为x轴，体能成绩为y轴，画出散点图。
import pandas as pd
import numpy as np
from pandas import DataFrame as df
import matplotlib.pyplot as plt
import math
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False # 设置matplotlib正常显示中文和负号
#体育成绩用set方法进行量化
def set(pe):
    for i in range(len(pe)):
        if pe[i]=="excellent":
            pe[i]=95
        if pe[i]=="good":
            pe[i]=80
        if pe[i]=="general":
            pe[i]=65
        if pe[i]=="bad":
            pe[i]=45
df=pd.read_csv(r'E:\桌面\AllData.csv',encoding='gbk',header=0)
x=df.C1       #C1成绩
y=df.Constitution  #体育成绩
C1_list=list(x)
PE_list=list(y)
set(PE_list)
plt.scatter(C1_list,PE_list,c='blue',marker='x')
plt.title("课程1——体能成绩散点图")
plt.xlabel("C1")
plt.ylabel("Constitution")
plt.savefig('E:\桌面\散点图.png',bbox_inches='tight')
plt.show()

#2、以5分为间隔，画出课程1的成绩直方图。
bins=[60,65,70,75,80,85,90,95,100]  #设置间隔
plt.hist(x,edgecolor='blue',bins=bins)
plt.title('课程C1成绩直方图')
plt.grid(True)
plt.savefig('E:\桌面\直方图.png',dpi=300,bbox_inches='tight')
plt.show()

#3. 对每门成绩进行z-score归一化，得到归一化的数据矩阵。
list=[]   #存放所有成绩的列表，是二维列表
list.append(df.C1.tolist())
list.append(df.C2.tolist())
list.append(df.C3.tolist())
list.append(df.C4.tolist())
list.append(df.C5.tolist())
list.append(df.C6.tolist())
list.append(df.C7.tolist())
list.append(df.C8.tolist())
list.append(df.C9.tolist())
PE_sum=0
PE_list=[]
for i in range(len(df)):
    if df.Constitution[i] == "bad":
        j=45
        PE_sum+=j
        PE_list.append(j)
    elif df.Constitution[i] == "general":
        j = 65
        PE_sum += j
        PE_list.append(j)
    elif df.Constitution[i] == "good":
        j = 80
        PE_sum += j
        PE_list.append(j)
    elif df.Constitution[i] == "excellent":
        j = 90
        PE_sum += j
        PE_list.append(j)
PE_average=PE_sum/len(df) #体育成绩平均值
list.append(PE_list)
PE_SUM=0  #体育成绩-体育成绩平均值然后平方，最后所有项求和

for i in list[9]:
    PE_SUM+=(list[9][i]-PE_average)**2
PE_var=np.sqrt(PE_SUM/len(df))    #PE_var表示体育成绩标准差

j=0
#每一列进行z-score归一化，j表示列数
while j<10:
    if j<9:
        average=df["C"+str(j+1)].mean()
        var=df["C"+str(j+1)].std()
        for i in range(len(df)):
            list[j][i]=(list[j][i]-average)/var
    else:
        average=PE_average
        var=PE_var
        for i in range(len(df)):
            list[j][i] = (list[j][i] - average) / var
    j+=1

data=np.mat(list) #用data形成list矩阵
data_mat=data.T   #data_mat用来存data矩阵的转置，这样data_mat就是归一化后的数据矩阵
# print(data_mat[0])
df1=pd.DataFrame(data=data_mat)
df1.to_csv('zscore_data.txt',sep='\t',header=False,index=False)
