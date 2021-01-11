import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import seaborn as sns
import copy

##数据全显示
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)
pd.set_option("display.max_columns",None)
pd.set_option("display.max_rows",None)


##绘图时可以显示中文
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

##去除省略号
np.set_printoptions(threshold=np.inf)


# #读数据
filepath=r"C:\Users\hp\Desktop\AllData(1).csv"
df=pd.read_csv(filepath,encoding="gbk",header=0,engine="python")


list1=[]  #二维矩阵存放数据源的每一列成绩
list1.append(df.C1.tolist())
list1.append(df.C2.tolist())
list1.append(df.C3.tolist())
list1.append(df.C4.tolist())
list1.append(df.C5.tolist())
list1.append(list(map(lambda x:x*10,df.C6.tolist())))
list1.append(list(map(lambda x:x*10,df.C7.tolist())))
list1.append(list(map(lambda x:x*10,df.C8.tolist())))
list1.append(list(map(lambda x:x*10,df.C9.tolist())))
PE_list=[]
for i in range(len(df)):
    if df.Constitution[i] == "bad":
        j=random.randint(60,69)
        PE_list.append(j)
    elif df.Constitution[i] == "general":
        j = random.randint(70, 79)
        PE_list.append(j)
    elif df.Constitution[i] == "good":
        j = random.randint(80, 89)
        PE_list.append(j)
    elif df.Constitution[i] == "excellent":
        j = random.randint(90, 99)
        PE_list.append(j)
list1.append(PE_list)
data1=np.mat(list1)   #data1用来存放list1矩阵
data1_mat=data1.T #data1转置就可以得到行表示学生，列表示成绩的矩阵
list_avg=[]   #存放每个学生的成绩平均值
for i in range(len(data1_mat)):
    sum=0 #一个学生的成绩和
    for j in range(10):
        sum+=data1_mat[i,j]
    list_avg.append(sum/10.0)
# print(len(list_avg))

list_var=[]   #每个学生成绩的标准差
for i in range(len(data1_mat)):
    sum=0 #一个学生的成绩-平均值然后平方，最后所有项求和
    for j in range(10):
        sum+=((data1_mat[i,j]-list_avg[i])**2)
    list_var.append(np.sqrt(sum/9.0))
# print(list_var)
cor_mat=np.mat(np.zeros((len(data1_mat),len(data1_mat)))) #先生成一个以学生数量为阶的全0方阵，之后替换里面元素变为相关矩阵
# print(len(cor_mat[0]))

def corvar(i,j):
#计算两个学生即两行的协方差
#运用公式cov（x，y）=E[（x-E（x)*(y-E(y))]
    stu1=[]   #存放第i行的成绩-其对应平均值的列表
    stu2=[]   #存放第j行的成绩-其对应平均值的列表
    for k in range(10):
        stu1.append(data1_mat[i,k]-list_avg[i])
        stu2.append(data1_mat[j,k]-list_avg[j])
    sum=0 #stu1和stu2元素按照下标对应相乘后加起来
    for k in range(10):
        sum+=stu1[k]*stu2[k]
    # print(stu1)
    # print(stu2)
    return sum/9.0    #返回协方差
# t=corvar(0,1)
# cor_mat[0,1]=t/(list_var[0]*list_var[1])
for i in range(len(data1_mat)):
    for j in range(len(data1_mat)):
        t=corvar(i,j)
        # print(t)
        cor_mat[i,j]=t/(list_var[i]*list_var[j])  #cor_mat[i,j]表示第i行第j行的相关系数
# print(cor_mat)
# df2=pd.DataFrame(data=cor_mat)
# df2.to_csv('exp2-5-Correlation Matrix.csv',sep=',',header=False,index=False)
plt.figure(figsize=(20,20),dpi=80)
sns.heatmap(cor_mat,vmin=-1,vmax=1,linewidths=0.08,xticklabels=False,cmap='coolwarm') #可视化相关矩阵，用热点图
plt.savefig('exp2-4-heatmap.png',dpi=100,bbox_inches='tight')
plt.show()



a=copy.deepcopy(cor_mat)
# b=np.argsort(a[0],axis=1)
# print(b[0,len(a)-2])
# print(a[0,b[0,len(a)-2]])
# print(b)
# print(a[0])
maxlist=[]
id=[]
for i in range(len(a)):
    p=[]
    l=[]
    b=np.argsort(a[i],axis=1)
    p.append(a[i,b[0,len(a)-2]])
    p.append(a[i, b[0, len(a) - 3]])
    p.append(a[i, b[0, len(a) - 4]])
    maxlist.append(p)
    l.append(df.ID[b[0,len(a)-2]])
    l.append(df.ID[b[0, len(a) - 3]])
    l.append(df.ID[b[0, len(a) - 4]])
    id.append(l)
# print(maxlist)
id_mat=np.mat(id)
# print(id_mat)
dfid=pd.DataFrame(data=id_mat)
print(dfid)
dfid.to_csv('exp2-5-detail.txt',sep='\t',index=False,header=False)
