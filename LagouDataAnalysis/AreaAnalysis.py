import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Simhei']#中文显示
plt.rcParams['axes.unicode_minus'] = False #显示负号

def get_industry_dict(field_series):
    industry_dict={}
    for field in list(field_series):
        labels = str(field).strip().replace('020', 'O2O').replace(' ', ',').replace('、', ',').split(',')
        for label in labels:
            if label!='':
                #如果行业标签已经出现在industry_dict字典里面，在原来的基础上+1
                #如果没有出现出现，就初始化为1
                if label in industry_dict.keys():
                    industry_dict[label] += 1
                else:
                    industry_dict[label]=1
    return industry_dict

def get_city_img(cities):
    city_count=cities.value_counts()#统计频数
    city_count_hot=city_count[city_count>80]#保留大于80的城市
    city_count_other=pd.Series(city_count[city_count<=80].sum(),index=['其他'])#小于80的城市进行求和
    city_counts=pd.concat([city_count_hot,city_count_other])#合并
    city_pro = (city_counts.div(city_counts.sum())*100).round(1)#计算频率
    labels=list(city_pro.index)
    plt.figure(figsize=(10,10))
    #绘制饼状图
    patches, texts, autotexts=plt.pie(list(city_pro),labels=labels,autopct='%0.1f%%')
    for t in texts:#标签大小
        t.set_size(15)
    for t in autotexts:#数字标签大小
        t.set_size(12)
    plt.title('数据分析师地域分布',fontsize=20)
    plt.savefig('imge/AreaDistribute.png',dpi=300,bbox_inches='tight')
    # plt.show()

def get_work_year(workYears):
    workYear_count = workYears.value_counts()[:-1]#统计每个经验需求的数量
    workYear_rate = (workYear_count.div(workYear_count.sum())*100).round(1)#获取对应的百分比
    labels = list(workYear_rate.index)
    plt.figure(figsize=(10, 10))
    #画饼状图
    patches, texts, autotexts = plt.pie(list(workYear_rate), labels=labels, autopct='%0.1f%%')
    #修改标签的字体大小
    for t in texts:
        t.set_size(15)
    #修改数字标签的字体大小
    for t in autotexts:
        t.set_size(12)
    plt.title('数据分析师工作年限分布', fontsize=20)
    plt.savefig('imge/WorkYearDistribute.png', dpi=300, bbox_inches='tight')#保存图片

def get_industry_field(industry_dict):
    industry_Series=pd.Series(industry_dict).sort_values(ascending=False)#转化为Series对象
    industry_hot=industry_Series[industry_Series>120]#保留大于120的数量
    industry_other=pd.Series(industry_Series[industry_Series<=120].sum(),index=['其他'])#将小于120的数量求和，转化为Series对象
    industry_hot=industry_hot.append(industry_other)#合并
    industry_rate = (industry_hot.div(industry_hot.sum())*100).round(1)#每个行业对应的求频率
    labels = list(industry_rate.index)
    plt.figure(figsize=(10, 10))
    # 画饼状图
    patches, texts, autotexts = plt.pie(list(industry_rate), labels=labels, autopct='%0.1f%%')
    # 修改标签的字体大小
    for t in texts:
        t.set_size(15)
    # 修改数字标签的字体大小
    for t in autotexts:
        t.set_size(12)
    plt.title('数据分析师行业分布', fontsize=20)
    plt.savefig('imge/IndustryFieldDistribute.png', dpi=300, bbox_inches='tight')  # 保存图片

if __name__=='__main__':
    data = pd.read_csv('data/LagouPostion.csv',encoding='gb18030')
    data = data[data['jobNature']=='全职']
    get_city_img(data['city'])#绘制城市分布
    get_work_year(data['workYear'])#绘制工作年限分布
    industry_dict=get_industry_dict(data['industryField'])#行业的频数
    get_industry_field(industry_dict)#绘制行业分布图
