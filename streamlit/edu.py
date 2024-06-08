
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager, FontProperties

def getEduPic(df):
    # 假设你的自定义字体名为 'MyCustomFont.ttf'，并且该字体文件位于当前工作目录
    custom_font_path = 'simfang.ttf'
     
    # 将自定义字体添加到 matplotlib 的字体列表中
    matplotlib.font_manager.fontManager.addfont(custom_font_path)
     
    # 创建一个 FontProperties 对象来指定字体
    font = FontProperties(fname=custom_font_path, size=14)

    # 确保文件路径正确
    #file_path = r'F:\dataAny\\alldata.csv'

    # 读取CSV文件
    #df = pd.read_csv(file_path)

    # 提取教育背景列
    edu_counts = df['EDU'].value_counts()
    print(edu_counts)
    # 标签和对应的数量
    labels = edu_counts.index
    sizes = edu_counts.values
    print(labels,sizes)
    # 颜色
    colors = plt.cm.Paired(range(len(labels)))

    # 创建fig和ax对象
    fig, ax = plt.subplots()

    # 绘制饼图
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

    # 确保饼图是圆形的
    ax.axis('equal')

    # 标题
    ax.set_title('教育背景分布', fontsize=20, color="brown",fontproperties=font)

    # 保存图表
    # fig.savefig("教育背景分布图1.png", dpi=300)
    #print("save!!!!")
    plt.show()

    # 返回fig对象
    return fig


def plot_gender_distribution(df):
    matplotlib.font_manager.fontManager.addfont('SimHei.ttf') 
    
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    
    plt.rcParams['axes.unicode_minus']=False#用来正常显示负号
    # 提取性别列
    gender_counts = df['GENDER'].value_counts()

    # 标签和对应的数量
    labels = gender_counts.index
    sizes = gender_counts.values

    # 颜色
    colors = ['skyblue', 'lightcoral']



    # 创建fig和ax对象
    fig, ax = plt.subplots()

    # 绘制饼图
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=140)

    # 确保饼图是圆形的
    ax.axis('equal')

    # 标题
    ax.set_title('男女分布占比', fontsize=20, color='brown')

    # 返回fig对象
    return fig


def plot_most_used_apps(df):

    matplotlib.font_manager.fontManager.addfont('SimHei.ttf') 
    
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    
    plt.rcParams['axes.unicode_minus']=False#用来正常显示负号
    # 提取最常使用程序的数据
    most_used_apps = df['最常使用的程序'].value_counts().head(10)

    # 标签和对应的数量
    labels = most_used_apps.index
    sizes = most_used_apps.values

    # 创建fig和ax对象
    fig, ax = plt.subplots()

    # 绘制水平条形图
    colors = plt.cm.Paired(range(len(labels)))
    ax.barh(labels, sizes, color=colors)
    ax.invert_yaxis()

    # 添加标签和标题
    ax.set_xlabel('使用次数')
    ax.set_ylabel('程序')
    ax.set_title('最常使用的程序', fontsize=20, color='brown')

    # 返回fig对象
    return fig
