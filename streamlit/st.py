import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from dashvector import Client
import folium
from matplotlib import colormaps, pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import matplotlib

font = {'family': 'Microsoft YaHei', 'weight': 'bold'}
matplotlib.rc("font", **font)


def getmap(province_values):
    if isinstance(province_values, pd.Series):
        provinces = province_values.index.tolist()
        values = province_values.values.tolist()
    elif isinstance(province_values, dict):
        provinces = list(province_values.keys())
        values = list(province_values.values())
    else:
        raise ValueError("province_values must be a pandas.Series or a dictionary.")

    dict = [
        {"province": "上海", "lats": 31.230416, "lons": 121.473701},
        {"province": "云南", "lats": 24.679438, "lons": 102.832891},
        {"province": "内蒙古", "lats": 44.09333, "lons": 111.670801},
        {"province": "北京", "lats": 39.5424, "lons": 116.2351},
        {"province": "台湾", "lats": 23.69781, "lons": 120.960515},
        {"province": "吉林", "lats": 43.666368, "lons": 126.192314},
        {"province": "四川", "lats": 30.572269, "lons": 104.066541},
        {"province": "天津", "lats": 39.085111, "lons": 117.200983},
        {"province": "宁夏", "lats": 37.264608, "lons": 106.165917},
        {"province": "安徽", "lats": 31.861184, "lons": 117.284923},
        {"province": "山东", "lats": 36.682785, "lons": 117.020359},
        {"province": "山西", "lats": 37.877826, "lons": 112.562398},
        {"province": "广东", "lats": 23.132278, "lons": 113.266531},
        {"province": "广西", "lats": 22.815478, "lons": 108.327546},
        {"province": "新疆", "lats": 43.793026, "lons": 87.627704},
        {"province": "江苏", "lats": 32.061707, "lons": 118.767413},
        {"province": "江西", "lats": 28.676493, "lons": 115.892151},
        {"province": "河北", "lats": 38.045475, "lons": 114.502461},
        {"province": "河南", "lats": 34.757977, "lons": 113.665412},
        {"province": "浙江", "lats": 30.26555, "lons": 120.153576},
        {"province": "海南", "lats": 19.197625, "lons": 109.724438},
        {"province": "湖北", "lats": 30.584355, "lons": 114.298572},
        {"province": "湖南", "lats": 28.19409, "lons": 112.982279},
        {"province": "甘肃", "lats": 36.059089, "lons": 103.826308},
        {"province": "福建", "lats": 26.078498, "lons": 119.306239},
        {"province": "贵州", "lats": 26.647661, "lons": 106.630154},
        {"province": "辽宁", "lats": 41.835558, "lons": 123.429096},
        {"province": "重庆", "lats": 29.56301, "lons": 106.551556},
        {"province": "陕西", "lats": 34.265472, "lons": 108.954239},
        {"province": "青海", "lats": 36.625657, "lons": 101.780199},
        {"province": "黑龙江", "lats": 45.742347, "lons": 126.661669}
    ]

    # 从字典中提取经纬度
    lats = [d['lats'] for d in dict]
    lons = [d['lons'] for d in dict]

    # 创建地图对象
    map = folium.Map(location=[35, 105], zoom_start=4)

    # 使用matplotlib colormap生成颜色序列
    cmap = colormaps['viridis']  # 使用新方法访问colormap
    norm = plt.Normalize(min(values), max(values))  # 归一化values以便映射到颜色序列

    # 在地图上添加每个省份的标记
    for i, (province, value) in enumerate(zip(provinces, values)):
        province_data = next((d for d in dict if d["province"] == province), None)
        if province_data:
            lat, lon = province_data["lats"], province_data["lons"]
            # 根据value映射颜色
            color = cmap(norm(value))
            hex_color = '#{0:02x}{1:02x}{2:02x}'.format(*[int(c * 255) for c in color[:3]])

            folium.Circle(
                location=[lat, lon],
                radius=value * 5000,  # 根据数值调整半径大小
                color=hex_color,
                fill=True,
                fill_color=hex_color,
                fill_opacity=0.5
            ).add_child(folium.Popup(province + ': ' + str(value))).add_to(map)
        else:
            print(f"未找到省份 '{province}' 的经纬度数据")

    # 保存地图为HTML文件
    map.save('map.html')


st.set_page_config(layout="wide")


def getQueryUser(queryId):
    client = Client(
        api_key='sk-WnUvx6e64txy8IaGkATNcfeGGa9oJB3DCAF8E129B11EF822C8AC4FB9F1729',
        endpoint='vrs-cn-83l3qpgwq0003e.dashvector.cn-hangzhou.aliyuncs.com'
    )
    collection = client.get(name='USER')
    ret = collection.query(
        id=queryId,
        topk=6,
    )
    # 判断query接口是否成功
    if ret:
        print('query success')
        # print(ret)
    return ret


# Load the data
# 确保文件路径正确
file_path = r'alldata.csv'
data = pd.read_csv(file_path)

# Title
st.title('数据可视化')

# User input for USERID
user_id_input = st.text_input('请输入用户ID以查询用户信息：')

# Filter the data for the specified USERID
user_data = data[data['USERID'] == user_id_input]

# Check if the USERID exists in the data
if user_data.empty:
    st.write('未找到指定的用户ID。')
else:
    # Combine the selected columns into a single string for word cloud generation
    selected_columns = ['GENDER', 'BIRTHDAY', 'EDU', 'JOB', 'INCOME', 'CITY', 'PROVINCE', '最常使用的程序',
                        '基础活跃时段分类', '用户类别标签', '会话行为特征', '技术适应能力',
                        '活跃程度', '多样性使用者', '用户类别', '软件多样性与偏好', '操作复杂度', '应用使用细化',
                        '安全与隐私意识', '互动频繁度']
    llm_explain_columns = ['模型所给的响应', '用户行为分析']
    # Combine the selected columns into a single string for word cloud generation
    user_profile_text = ' '.join(user_data[selected_columns].iloc[0].dropna().astype(str).values)
    llm_explain_text = '\n\n#### 网页访问情况:\n'.join(
        user_data[llm_explain_columns].iloc[0].dropna().astype(str).values)
    st.write("### 大模型解析:")
    st.write(llm_explain_text)

    st.subheader('用户词云')
    mask = plt.imread(r"F:\下载\article\用户管理.jpg")  # 读取遮罩图片
    # Generate the word cloud
    wordcloud = WordCloud(font_path=r'C:\Windows\Fonts\simfang.ttf', width=500, height=500, mask=mask,
                          background_color='white').generate(user_profile_text)
    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

st.subheader('用户推荐网络')
if user_id_input:
    ret = getQueryUser(user_id_input)
    col0, col1 = st.columns([0.5, 0.5])

    nodes = []
    edges = []
    for data in ret:
        nodes.append(
            Node(id=data.id,
                 label=data.id,
                 size=25,
                 shape="circularImage",
                 image=r"https://th.bing.com/th/id/OIP.jzp7hoIBz4-yQ1UFn4FY1AHaHa?rs=1&pid=ImgDetMain")
        )
    userId = ret[0].id
    index = 0
    for data in ret:
        if index == 0:
            index = index + 1
            continue
        edges.append(Edge(source=userId,
                          label=f"{data.score}",
                          target=data.id,
                          )
                     )
    config = Config(width=1000,
                    height=1000,
                    directed=False,
                    physics=False,
                    hierarchical=True,
                    # **kwargs
                    )

    return_value = agraph(nodes=nodes,
                          edges=edges,
                          config=config)
    st.write(return_value)
    with col0:
        if ret[0].id:
            data = pd.read_csv(file_path)
            user_data1 = data[data['USERID'] == ret[0].id]
            # Combine the selected columns into a single string for word cloud generation
            selected_columns = ['GENDER', 'BIRTHDAY', 'EDU', 'JOB', 'INCOME', 'CITY', 'PROVINCE', '最常使用的程序',
                                '基础活跃时段分类', '用户类别标签', '会话行为特征', '技术适应能力',
                                '活跃程度', '多样性使用者', '用户类别', '软件多样性与偏好', '操作复杂度',
                                '应用使用细化',
                                '安全与隐私意识', '互动频繁度']
            llm_explain_columns = ['模型所给的响应', '用户行为分析']
            # Combine the selected columns into a single string for word cloud generation
            user_profile_text = ' '.join(user_data1[selected_columns].iloc[0].dropna().astype(str).values)
            llm_explain_text = '\n\n#### 网页访问情况:\n'.join(
                user_data1[llm_explain_columns].iloc[0].dropna().astype(str).values)
            st.write("## 用户:")
            st.write("### 大模型解析:")
            st.write(llm_explain_text)

            st.subheader('用户词云')
            mask = plt.imread(r"F:\下载\article\用户管理.jpg")  # 读取遮罩图片
            # Generate the word cloud
            wordcloud = WordCloud(font_path=r'C:\Windows\Fonts\simfang.ttf', width=500, height=500, mask=mask,
                                  background_color='white').generate(user_profile_text)
            # Display the word cloud
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(plt)
    with col1:
        if ret[2].id:
            data = pd.read_csv(file_path)
            user_data2 = data[data['USERID'] == ret[1].id]
            # Combine the selected columns into a single string for word cloud generation
            selected_columns = ['GENDER', 'BIRTHDAY', 'EDU', 'JOB', 'INCOME', 'CITY', 'PROVINCE', '最常使用的程序',
                                '基础活跃时段分类', '用户类别标签', '会话行为特征', '技术适应能力',
                                '活跃程度', '多样性使用者', '用户类别', '软件多样性与偏好', '操作复杂度',
                                '应用使用细化',
                                '安全与隐私意识', '互动频繁度']
            llm_explain_columns = ['模型所给的响应', '用户行为分析']
            # Combine the selected columns into a single string for word cloud generation
            user_profile_text = ' '.join(user_data2[selected_columns].iloc[0].dropna().astype(str).values)
            llm_explain_text = '\n\n#### 网页访问情况:\n'.join(
                user_data2[llm_explain_columns].iloc[0].dropna().astype(str).values)
            st.write("## 推荐好友:")
            st.write("### 大模型解析:")
            st.write(llm_explain_text)
            st.subheader('用户词云')
            mask = plt.imread(r"F:\下载\article\用户管理.jpg")  # 读取遮罩图片
            # Generate the word cloud
            wordcloud = WordCloud(font_path=r'C:\Windows\Fonts\simfang.ttf', width=500, height=500, mask=mask,
                                  background_color='white').generate(user_profile_text)
            # Display the word cloud
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(plt)

# Display the user data
if not user_data.empty:
    st.subheader('用户数据')
    st.write(user_data)

# Sidebar for selecting features
st.sidebar.title('筛选器')
gender = st.sidebar.multiselect('性别', data['GENDER'].unique(), default=data['GENDER'].unique())
education = st.sidebar.multiselect('教育程度', data['EDU'].unique(), default=data['EDU'].unique())
occupation = st.sidebar.multiselect('职业', data['JOB'].unique(), default=data['JOB'].unique())
income = st.sidebar.multiselect('收入', data['INCOME'].unique(), default=data['INCOME'].unique())
province = st.sidebar.multiselect('省份', data['PROVINCE'].unique(), default=data['PROVINCE'].unique())

# Age selection
min_age, max_age = st.sidebar.slider('年龄', int(data['BIRTHDAY'].min()), int(data['BIRTHDAY'].max()),
                                     (int(data['BIRTHDAY'].min()), int(data['BIRTHDAY'].max())))

# Filter the data based on the selected features
filtered_data = data[
    (data['GENDER'].isin(gender if gender else data['GENDER'].unique())) &
    (data['BIRTHDAY'] >= min_age) &
    (data['BIRTHDAY'] <= max_age) &
    (data['EDU'].isin(education if education else data['EDU'].unique())) &
    (data['JOB'].isin(occupation if occupation else data['JOB'].unique())) &
    (data['INCOME'].isin(income if income else data['INCOME'].unique())) &
    (data['PROVINCE'].isin(province if province else data['PROVINCE'].unique()))
    ]



# Display the number of users after filtering
st.write(f'筛选后的用户数量: {len(filtered_data)}')
# Display key statistics
st.subheader('关键统计数据')
st.write(filtered_data.describe(include='all'))

col3,col4=st.columns([0.5,0.5])
with col3:
    # Visualizations
    st.subheader('性别分布')
    from edu import plot_gender_distribution
    fig = plot_gender_distribution(filtered_data)
    st.pyplot(fig)

with col4:
    st.subheader('年龄分布')
    plt.figure(figsize=(10, 5))
    plt.hist(filtered_data['BIRTHDAY'], bins=range(int(data['BIRTHDAY'].min()), int(data['BIRTHDAY'].max()) + 1),
             align='left', rwidth=0.8)
    plt.xlabel('birth')
    plt.ylabel('num')
    st.pyplot(plt)

col5,col6=st.columns([0.5,0.5])
with col5:
    st.subheader('教育程度分布')
    from edu import getEduPic
    fig = getEduPic(filtered_data)
    st.pyplot(fig)
with col6:
    st.subheader('收入分布')
    income_counts = filtered_data['INCOME'].value_counts()
    st.bar_chart(income_counts)

col7,col8=st.columns([0.5,0.5])
with col7:
    st.subheader('职业分布')
    occupation_counts = filtered_data['JOB'].value_counts()
    st.bar_chart(occupation_counts)

with col8:
    st.subheader('最常使用程序分布（Top10）')
    from edu import plot_most_used_apps
    fig = plot_most_used_apps(filtered_data)
    st.pyplot(fig)

# getmap([],[])


st.subheader('省份分布')
province_counts = filtered_data['PROVINCE'].value_counts()

getmap(province_counts)
# 加载HTML文件并展示
with open("map.html", "r", encoding="utf-8") as f:
    map_html = f.read()

st.components.v1.html(map_html, height=600)

# Display the filtered data
st.subheader('筛选后的数据')
st.write(filtered_data)
