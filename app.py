import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# 设置页面标题
st.set_page_config(page_title="我的第一个交互工具", layout="wide")

# 标题
st.title("🎯 我的第一个 Streamlit 交互工具")
st.markdown("这是一个简单的演示，展示如何创建交互式分析工具")

# 侧边栏
with st.sidebar:
    st.header("⚙️ 参数设置")
    num_points = st.slider("数据点数量", 100, 10000, 1000)
    noise_level = st.slider("噪点级别", 0.1, 2.0, 1.0)
    chart_type = st.selectbox("图表类型", ["散点图", "折线图", "直方图"])

# 生成模拟数据
st.header("📊 数据分析展示")
st.write(f"当前设置：{num_points} 个数据点，噪点级别 {noise_level}")

# 创建两列布局
col1, col2 = st.columns(2)

with col1:
    st.subheader("数据表格")
    # 生成模拟数据
    np.random.seed(42)
    data = pd.DataFrame({
        'X': np.random.randn(num_points),
        'Y': np.random.randn(num_points) * noise_level,
        '类别': np.random.choice(['A', 'B', 'C'], num_points)
    })
    
    # 添加一些计算列
    data['距离'] = np.sqrt(data['X']**2 + data['Y']**2)
    data['角度'] = np.arctan2(data['Y'], data['X'])
    
    st.dataframe(data.head(10), use_container_width=True)
    st.caption(f"总数据量：{len(data)} 行")

with col2:
    st.subheader("数据统计")
    st.write("基本统计信息：")
    st.json({
        "X均值": float(data['X'].mean()),
        "Y均值": float(data['Y'].mean()),
        "X标准差": float(data['X'].std()),
        "Y标准差": float(data['Y'].std())
    })

# 图表展示
st.header("📈 可视化图表")

# 根据选择显示不同图表
if chart_type == "散点图":
    fig = px.scatter(data, x='X', y='Y', color='类别', 
                     title=f"散点图 (n={num_points})",
                     opacity=0.7)
elif chart_type == "折线图":
    fig = px.line(data.sort_values('X').head(100), x='X', y='Y', 
                  title="折线图（前100个点）")
else:  # 直方图
    fig = px.histogram(data, x='距离', nbins=30, 
                       title="距离分布直方图")

st.plotly_chart(fig, use_container_width=True)

# 交互功能
st.header("🔧 交互功能演示")

tab1, tab2, tab3 = st.tabs(["文件上传", "实时计算", "信息展示"])

with tab1:
    uploaded_file = st.file_uploader("上传CSV文件（可选）", type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(f"文件已上传！大小：{len(df)} 行 × {len(df.columns)} 列")
        st.write("前5行数据：")
        st.dataframe(df.head())
        
        # 让用户选择要可视化的列
        if len(df.columns) >= 2:
            col_x = st.selectbox("选择X轴", df.columns)
            col_y = st.selectbox("选择Y轴", df.columns)
            if col_x and col_y:
                fig2 = px.scatter(df, x=col_x, y=col_y)
                st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("实时计算示例")
    a = st.number_input("输入数值 A", value=10.0)
    b = st.number_input("输入数值 B", value=5.0)
    
    if st.button("开始计算"):
        with st.spinner("计算中..."):
            time.sleep(1)  # 模拟计算耗时
            result = a + b
            st.success(f"A + B = {result}")
            
            # 更多计算
            st.metric("A × B", f"{a * b:.2f}")
            st.metric("A ÷ B", f"{a / b:.2f}" if b != 0 else "无穷大")

with tab3:
    st.subheader("工具介绍")
    st.info("这是一个用 Streamlit 构建的交互式分析工具演示。")
    st.markdown("""
    ### 已实现功能：
    - ✅ 交互式参数调整
    - ✅ 数据可视化
    - ✅ 文件上传处理
    - ✅ 实时计算
    - ✅ 响应式布局
    
    ### 技术栈：
    - **Streamlit** - 前端框架
    - **Plotly** - 可视化库
    - **Pandas** - 数据处理
    - **NumPy** - 数值计算
    """)
    
    if st.checkbox("显示源代码预览"):
        st.code("""
# Streamlit 应用的基本结构
import streamlit as st

# 添加交互组件
user_input = st.slider("选择数值", 0, 100, 50)

# 显示结果
st.write(f"你选择了: {user_input}")
        """, language="python")

# 底部信息
st.divider()
st.caption("最后更新: 2024年 | 这是一个演示项目")