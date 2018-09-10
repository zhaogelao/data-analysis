import jieba
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS
from SalaryAnalysis import deal_salary
import re
from matplotlib import cm

#中文停用词
def get_stopword():
    stopword=[]
    filename = 'data/中文停用词库.txt'
    for line in open(filename,'r'):
        line = line.strip()
        if line != '':
            stopword.append(line)
    return stopword

#处理职责描述，进行结巴分词
def deal_description(description):
    description=description.replace('\xa0','').replace('一','').replace('职位描述：','').replace('\r\n','').replace('岗位','').replace('职责','').replace('要求','').strip()
    seg_list=jieba.cut(description)
    return seg_list

#词频统计
def word_count(description_series):
    word_dict={}
    stopword = get_stopword()#停用词
    for description in list(description_series):#传入的是一个Series对象，对每个元素进行处理
        for word in description:#每个元素都是列表对象，进行循环
            word = word.strip().upper()
            #通过正则表达式，去除非中文字符
            pattern=re.compile('[^\u4E00-\u9FEF]')
            word = re.sub(pattern,'',word)
            li =['数据','分析','数据分析']#频数比较高的词汇
            if len(word)>0 and word not in stopword and word != ''and word not in li:
                if word in word_dict.keys():#如果已经存在字典里面，则+1
                    word_dict[word]+=1
                else:#如果不在，则初始化为1
                    word_dict[word]=1
    return word_dict

#绘制词云图，下面两个链接为参考
#https://blog.csdn.net/fly910905/article/details/77763086
#https://blog.csdn.net/yaochuyi/article/details/80094659
def get_word_description_img(word_dict):
    back=plt.imread('data/back.jpg')#导入背景图
    wc = WordCloud(
        background_color='white',# 设置背景颜色
        mask=back,#设置背景图
        font_path='C:\Windows\Fonts\simhei.ttf',
        max_words=1000,#最多词数
        max_font_size=1000,#最大字体
        stopwords=STOPWORDS,
        colormap=cm.cool,#给每个单词随机分配颜色
        random_state=150#为每个单词返回一个PIL颜色
    )
    wc.generate_from_frequencies(word_dict)#根据词频生成词云
    plt.imshow(wc)# 显示词云图
    plt.axis('off')#去除坐标轴
    plt.savefig('imge/Description.png',dpi=300)#保存

if __name__ == '__main__':
    data = pd.read_csv('data/LagouPosition1234.csv', encoding='gb18030')
    data = data[data['jobNature'] == '全职']
    data['description1'] = data['description'].apply(deal_description)#进行分词
    word_dict=word_count(data['description1'])#统计词频
    get_word_description_img(word_dict)#绘制词云