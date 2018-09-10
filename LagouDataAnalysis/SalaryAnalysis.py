import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Simhei']#中文显示
plt.rcParams['axes.unicode_minus'] = False #显示负号

#薪酬处理
def deal_salary(salary):
    if '以上' in salary:
        return int(salary.strip().replace('k', '').replace('以上', ''))+2
    else:
        salaries=salary.strip().replace('k','').replace('K','').split('-')
        money= int(salaries[0])+(int(salaries[1])-int(salaries[0]))*0.2
        return money

#薪酬分布
def get_salery_distibute(salary):
    bins = [0,5,10,15,20,25,30,100]#
    labels = ['5k以下','5k-10k','10k-15k','15k-20k','20k-25k','25k-30k','30k以上']
    salary_series=pd.cut(salary,bins=bins,labels=labels).value_counts()#将薪酬进行离散化处理
    salary_series=pd.Series(salary_series,index=labels)#转为Series对象
    plt.figure(figsize=(10,8))
    salary_series.plot(kind='bar')#绘制柱状图
    plt.title('数据分析师薪资分布情况',fontsize=20)
    plt.xticks(rotation=30,fontsize=15)
    # salary.plot.hist(bins=20,density=True)
    # salary.plot(kind='kde',color='g')
    plt.savefig('imge/SalaryDistribute.png',dpi=300)#保存

#不同城市的的薪酬分布
def get_city_salery_distibute(df):
    city_salary=[]
    main_city = ['北京','上海','深圳','广州','杭州']#主要城市列表
    for city in main_city:
        city_salary.append(list(df[df['city']==city]['money']))#获取每个城市的薪酬列表
    plt.boxplot(city_salary,autorange=True)#绘制箱型图
    plt.xticks(range(1,len(main_city)+1),main_city,fontsize=15)
    plt.title('数据分析师不同城市的薪资分布情况', fontsize=20)
    plt.savefig('imge/CitySalaryDistribute.png', dpi=300)

def get_education_salary_distribute(df):
    education_salary=df.groupby('education')['money'].mean().sort_values().round(0)
    plt.figure(figsize=(12,8))
    education_salary.plot(kind='bar')
    plt.xticks(rotation=30,fontsize=15)
    plt.ylabel('薪酬（K/月）',fontsize=15)
    plt.xlabel('')
    x = range(len(education_salary))
    y = list(education_salary)
    for a,b in zip(x,y):
        plt.text(a,b+0.5,str(b), fontsize=12,horizontalalignment='center',verticalalignment='center')
    plt.title('数据分析师不同教育背景的薪酬分布',fontsize=20)
    plt.savefig('imge/EducationSalaryDistribute.png',dpi=300)

def get_workyear_salary_distribute(df):
    education_salary = df.groupby('workYear')['money'].mean().sort_values().round(0)
    plt.figure(figsize=(12, 8))
    education_salary.plot(kind='bar')
    plt.xticks(rotation=30, fontsize=15)
    plt.ylabel('薪酬（K/月）', fontsize=15)
    plt.xlabel('')
    x = range(len(education_salary))
    y = list(education_salary)
    for a, b in zip(x, y):
        plt.text(a, b + 0.5, str(b), fontsize=12, horizontalalignment='center', verticalalignment='center')
    plt.title('数据分析师不同工作年限的薪酬分布', fontsize=20)
    plt.savefig('imge/WorkYearSalaryDistribute.png', dpi=300)


if __name__=='__main__':
    data = pd.read_csv('data/LagouPostion.csv',encoding='gb18030')
    data = data[data['jobNature']=='全职']
    # print(data.head())
    data['money']=data['salary'].apply(deal_salary)#处理薪酬
    get_salery_distibute(data['money'])#薪酬分布
    get_city_salery_distibute(data[['money','city']])#不同城市的薪酬分布
    get_education_salary_distribute(data[['money','education']])#不同教育背景的薪酬分布
    get_workyear_salary_distribute(data[['money', 'workYear']])#不同工作年限的薪酬分布