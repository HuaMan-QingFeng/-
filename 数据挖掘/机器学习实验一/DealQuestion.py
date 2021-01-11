"""
    功能：解决提出的问题
    1.	学生中家乡在Beijing的所有课程的平均成绩。
    2.	学生中家乡在广州，课程1在80分以上，且课程10在9分以上的男同学的数量。
    3.	比较广州和上海两地女生的平均体能测试成绩，哪个地区的更强些？
    4.	学习成绩和体能测试成绩，两者的相关性是多少？
"""


import pandas as pd
import xlrd2
import math

#将数据打印出来

gyz = pd.read_excel('./AllData.xlsx',sheet_name='Sheet', header=0)
print(gyz)





#1. 学生中家乡在Beijing的所有课程的平均成绩。

print("============第一题===============")
# 要被group的列名
Beijing = gyz.loc[gyz['City']=='Beijing']

print("北京学生C1均值为： ",Beijing['C1'].mean() )   #计算每列均值
print("北京学生C2均值为： ",Beijing['C2'].mean() )   #计算每列均值
print("北京学生C3均值为： ",Beijing['C3'].mean() )   #计算每列均值
print("北京学生C4均值为： ",Beijing['C4'].mean() )   #计算每列均值
print("北京学生C5均值为： ",Beijing['C5'].mean() )   #计算每列均值
print("北京学生C6均值为： ",Beijing['C6'].mean() )   #计算每列均值
print("北京学生C7均值为： ",Beijing['C7'].mean() )   #计算每列均值
print("北京学生C8均值为： ",Beijing['C8'].mean() )   #计算每列均值
print("北京学生C9均值为： ",Beijing['C9'].mean() )   #计算每列均值



#2. 学生中家乡在广州，课程1在80分以上，且课程9在9分以上的男同学的数量。
print("============第二题===============")
Guangzhou = gyz.loc[gyz['City']=='Guangzhou']
GZ_sum = len(Guangzhou[(Guangzhou['C1'] >80 )&(Guangzhou['C9'] > 9)&(Guangzhou['Gender'] == 'boy')])
print("学生中家乡在广州，课程1在80分以上，且课程9在9分以上的男同学的数量为：",GZ_sum)


#3. 比较广州和上海两地女生的平均体能测试成绩，哪个地区的更强些？
print("============第三题===============")
def getCount(key, value):
    """设置一个条件及关键词，返回满足该条件的关键词的列表"""
    In_City = gyz[gyz[key] == value]
    return In_City

Guangzhou_Con = getCount('City', 'Guangzhou')
ShangHai_Con = getCount('City', 'Shanghai')
Con_GZ = Guangzhou_Con['Constitution']
Con_Sh = ShangHai_Con['Constitution']

# excellent = 2, good = 1, general = 0, bad =-1.
def score(Con_City):
    sum = 0
    people_sum = Con_City.count();
    for i in Con_City:
        if i == 'excellent':
            sum += 2
        elif i == 'good':
            sum += 1
        elif i == 'general':
            sum += 0
        elif i == 'bad':
            sum += -1
        else:
            people_sum -= 1
    return sum, people_sum


score_GZ, people_GZ = score(Con_GZ)
score_Sh, people_Sh = score(Con_Sh)
print("\nexcellent:2, good:1, general:0, bad:-1")
print("两地平均体能测试成绩：  广州：%0.3f    上海：%0.3f" % (score_GZ / people_GZ, score_Sh / people_Sh))
if score_GZ > score_Sh:
    print(" 广州 平均体能测试成绩更佳")
else:
    print(" 上海 平均体能测试成绩更佳")



#4. 学习成绩和体能测试成绩，两者的相关性是多少？（九门课的成绩分别与体能成绩计算相关性）
print("============第四题===============")
def score(key):
    """将体能成绩量化：excellent = 2, good = 1, general = 0, bad =-1."""
    sum = []
    for i in gyz[key]:
        if i == 'excellent':
            sum.append(2)
        elif i == 'good':
            sum.append(1)
        elif i == 'general':
            sum.append(0)
        elif i == 'bad':
            sum.append(-1)
        else:
            sum.append(0)
    return sum


def Avg(list):
    """计算平均值 avg(a)=（a1+a2+……+an)/n"""
    sum = 0
    nan_num = 0
    for i in list:
        if math.isnan(i):
            nan_num += 1
        else:
            sum += i
    return sum / (len(list) - nan_num)


def Cov(list):
    """计算标准差s
    协方差：s**2 = ((x1-avg(x))**2+(x2-avg(x))**2+……+(xn-avg(xn))**2)/(n-1)
    """
    result = 0
    nan_num = 0
    for i in list:
        if math.isnan(i):
            nan_num += 1
        else:
            result += (i - Avg(list)) ** 2
    return (result / (len(list) + nan_num)) ** 0.5


def course(row):
    """计算A‘ ：计算 a’ = (ak-mean(A))/std(A)"""
    list_a = []
    for col in gyz[row]:
        if math.isnan(col):
            list_a.append((80 - Avg(gyz[row])) / Cov(gyz[row]))
        else:
            list_a.append((col - Avg(gyz[row])) / Cov(gyz[row]))
    return list_a


def b():
    """计算B‘ ：计算 b’ = (bk-mean(B))/std(B)"""
    num = score('Constitution')
    sumb = []
    for col in num:
        sumb.append((col - Avg(num)) / Cov(num))
    return sumb


def solvequestion():
    """计算相关性；correlation(A,B) = A'* B' """
    key = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
    list_b = b()

    # 用课程每一列与体能成绩做相关性计算即：n*9矩阵 与 n*1矩阵 相乘
    for i in range(len(key)):
        list_a = course(key[i])
        for e in range(len(list_a)):
            sum = 0  # 计算结果
            # 一维矩阵做相乘
            for col in range(len(list_b)):
                temp = list_a[col] * list_b[col]  # 点积
                if math.isnan(list_a[col]):
                    print("发现nan")
                sum += temp
        print("\n%s 与 Constitution 的相关系数：%s" % (key[i], temp))


solvequestion()

