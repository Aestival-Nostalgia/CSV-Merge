# -*- coding: utf-8 -*-
from turtle import done
import pandas as pd
import os
import csv
 
inPath = r"D:\G\PRO"
outPath = r"D:\G\PRO2"
donePath = r"D:\G"
BASE_filename = r"D:\G\BASE.csv"

CsvFile = os.listdir(inPath)

# 代码第一部分对刚完成提取的CSV文件进行裁切，裁切掉不需要的行和列，只保留用地类型的代码和对应的栅格数量

for i in range(len(CsvFile)):
    with open(os.path.join(inPath,CsvFile[i])) as temp_f:
        # get No of columns in each line
        col_count = [len(l.split(",")) for l in temp_f.readlines()]
    column_names = [i for i in range(max(col_count))]
    df = pd.read_csv(os.path.join(inPath,CsvFile[i]),header = None,names=column_names)
    df = df.drop([0,1,2])
    df = df.drop([0,3],axis = 1)
    df[2] = df[2].astype('int') * 0.09 #这里要数据类型转换一下，用来把栅格数量换成面积
    df.to_csv(os.path.join(outPath,CsvFile[i]),index=False,encoding="utf-8",header = None)

print("PROCESSING_1 is Over!")

# 属于是自己学会for循环了，好几天的折磨总算是有所帮助
# 关于pandas包中read_csv函数里出现的某些问题可以参照：https://www.freesion.com/article/6737952790/  
# 开心！
# 基于Py3.7

# 接下来的工作，循环将多个CSV合并到已经设置好的主要CSV中
# 自己想办法写代码
# 成功了！多亏了pandas包的merge函数！

CsvFile_2 = os.listdir(outPath)
for i in range(len(CsvFile_2)):
    source_filename = os.path.join(outPath,CsvFile[i])
    source_file = pd.read_csv(source_filename,header = None)
    BASE_file = pd.read_csv(BASE_filename,header = None)
    mg = pd.merge(BASE_file,source_file,how="left",on=[0]) #注意，所有数据必须类型相同，另外，根据某一个键值进行匹配的时候，不要忘记用on命令。
    print(mg)
    mg.to_csv(BASE_filename, index = False, encoding="utf-8", header = None)
    
print("PROCESSING_2 is Over!")

#对拥有所有数据的主要CSV进行修改，包括添加一行表头，删除没有值的行，对删除后的空值格加零，最终生成一个新的Final CSV
