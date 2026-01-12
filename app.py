#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
评论分析智能体 - Web版本
基于Streamlit构建 - Apple极简风格
"""

import streamlit as st
from comment_analyzer import CommentAnalyzer

# 设置页面配置
st.set_page_config(
    page_title="用户声音洞察",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apple极简风格 CSS - 增强版（交互式动画设计）
st.markdown("""
<style>
    /* 全局样式重置 */
    .stApp {
        background: linear-gradient(135deg, #F5F5F7 0%, #E8E8ED 100%);
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Helvetica, Inter, Arial, sans-serif;
    }

    /* 关键帧动画定义 */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    @keyframes slideInFromTop {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.02);
        }
    }

    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    /* 隐藏侧边栏 */
    .stApp > header {
        visibility: hidden;
    }
    
    .stApp > header + div {
        visibility: hidden;
    }
    
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* 主要内容容器 - 限制宽度并居中 */
    .main .block-container {
        max-width: 800px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    
    /* 标题样式 - 添加动画效果 */
    .main-title {
        font-size: 3.5rem;
        font-weight: 500;
        color: #1d1d1f;
        text-align: center;
        letter-spacing: -0.02em;
        margin-bottom: 0.25rem;
        line-height: 1.1;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Helvetica, Inter, Arial, sans-serif;
        animation: slideInFromTop 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        background: linear-gradient(135deg, #1d1d1f 0%, #424245 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .subtitle {
        font-size: 1.125rem;
        font-weight: 400;
        color: #6e6e73;
        text-align: center;
        margin-bottom: 1.5rem;
        line-height: 1.5;
        animation: fadeIn 1s ease-out 0.3s both;
    }
    
    /* Main Stage 卡片容器 - 增强交互式设计 */
    .main-stage-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 28px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06), 0 2px 8px rgba(0, 0, 0, 0.04);
        padding: 2.5rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.6);
        animation: fadeInUp 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.2s both;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .main-stage-card:hover {
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.09), 0 4px 16px rgba(0, 0, 0, 0.06);
        transform: translateY(-2px);
    }
    
    /* 顶部 Expander 样式 - 纯文字链接样式 */
    .stExpander {
        border: none;
        background: transparent;
        margin-bottom: 1rem;
        box-shadow: none;
    }
    
    .stExpander summary {
        background: transparent !important;
        border: none !important;
        padding: 0.5rem 0 !important;
        font-size: 0.875rem;
        font-weight: 400;
        color: #6e6e73;
        cursor: pointer;
        list-style: none;
    }
    
    .stExpander summary:hover {
        color: #1d1d1f;
    }
    
    /* 隐藏默认的展开/收起图标 */
    .stExpander summary::-webkit-details-marker {
        display: none;
    }
    
    .stExpander summary::before {
        content: "▼";
        display: inline-block;
        margin-right: 0.5rem;
        font-size: 0.75rem;
        transition: transform 0.2s ease;
    }
    
    .stExpander[open] summary::before {
        transform: rotate(180deg);
    }
    
    .stExpander > div {
        background: transparent !important;
        border: none !important;
        padding: 1rem 0 !important;
        margin-top: 0.5rem;
    }
    
    /* Radio Button 样式优化 - 增强交互效果 */
    .stRadio > label {
        display: none !important;
    }

    .stRadio {
        margin-bottom: 1.25rem;
        animation: fadeIn 1s ease-out 0.5s both;
    }

    .stRadio [role="radiogroup"] {
        display: flex;
        gap: 0.75rem;
        justify-content: center;
        flex-wrap: wrap;
    }

    /* 强制Radio按钮文字为黑色，增强交互 */
    .stRadio [role="radiogroup"] > label {
        flex: 0 0 auto;
        font-size: 0.875rem;
        color: #1d1d1f !important;
        padding: 0.625rem 1.25rem;
        background: #F9F9F9;
        border: 1px solid #d2d2d7;
        border-radius: 14px;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        cursor: pointer;
        margin: 0;
        position: relative;
        overflow: hidden;
    }

    /* 添加微妙的光晕效果 */
    .stRadio [role="radiogroup"] > label::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(0, 0, 0, 0.05);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }

    .stRadio [role="radiogroup"] > label:hover {
        background: #f5f5f7;
        border-color: #1d1d1f;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    .stRadio [role="radiogroup"] > label:hover::before {
        width: 300px;
        height: 300px;
    }

    /* 选中状态的样式 */
    .stRadio [role="radiogroup"] > label[data-baseweb="radio"][aria-checked="true"],
    .stRadio [role="radiogroup"] > label[aria-checked="true"] {
        background: #000000 !important;
        color: #ffffff !important;
        border-color: #000000 !important;
        transform: translateY(0);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    }

    /* 确保Radio按钮内的文字可见 */
    .stRadio [role="radiogroup"] > label span {
        color: inherit !important;
        position: relative;
        z-index: 1;
    }
    
    /* 输入框样式 - 增强交互 */
    .stTextArea > label {
        display: none !important;
    }

    .stTextArea {
        margin-bottom: 1.5rem;
        animation: fadeInUp 1.1s cubic-bezier(0.16, 1, 0.3, 1) 0.4s both;
    }

    .stTextArea textarea {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Helvetica, Inter, Arial, sans-serif;
        font-size: 1rem;
        background-color: #FAFAFA;
        border: 1.5px solid #e5e5e7;
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        min-height: 280px;
        resize: vertical;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.02);
    }

    .stTextArea textarea:hover {
        border-color: #c7c7cc;
        background-color: #ffffff;
    }

    .stTextArea textarea:focus {
        outline: none;
        border-color: #1d1d1f;
        box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.05), inset 0 1px 3px rgba(0, 0, 0, 0.02);
        background-color: #ffffff;
        transform: scale(1.005);
    }

    .stTextArea textarea::placeholder {
        color: #86868b;
        font-size: 1rem;
        line-height: 1.5;
    }
    
    /* 按钮容器居中 */
    .button-container {
        display: flex;
        justify-content: center;
        margin: 1.5rem 0 0 0;
    }
    
    /* 按钮样式 - Apple风格微交互 */
    .stButton > button {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Helvetica, Inter, Arial, sans-serif;
        font-size: 1rem;
        font-weight: 500;
        background: linear-gradient(135deg, #000000 0%, #2c2c2e 100%);
        color: #ffffff;
        border: none;
        border-radius: 24px;
        padding: 0.875rem 2.5rem;
        min-width: 220px;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        cursor: pointer;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15), 0 2px 8px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 1.2s cubic-bezier(0.16, 1, 0.3, 1) 0.5s both;
    }

    /* 添加光泽效果 */
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.6s;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #1c1c1e 0%, #3a3a3c 100%);
        color: #ffffff;
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2), 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    .stButton > button:active {
        transform: translateY(0) scale(0.98);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* 结果区域样式 */
    .result-section {
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid #d2d2d7;
    }
    
    .result-section h2 {
        font-size: 1.5rem;
        font-weight: 500;
        color: #1d1d1f;
        margin-bottom: 1rem;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Helvetica, Inter, Arial, sans-serif;
    }
    
    .result-section h3 {
        font-size: 1.25rem;
        font-weight: 500;
        color: #1d1d1f;
        margin-top: 2rem;
        margin-bottom: 0.75rem;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Helvetica, Inter, Arial, sans-serif;
    }
    
    /* Markdown 表格样式 - 增强交互性 */
    .result-section table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 1rem 0;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Helvetica, Inter, Arial, sans-serif;
        font-size: 0.875rem;
        background-color: #ffffff;
        border: 1px solid #e5e5e7;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.3s both;
    }

    .result-section table th {
        background: linear-gradient(180deg, #fafafa 0%, #f5f5f7 100%);
        color: #1d1d1f;
        font-weight: 600;
        padding: 1rem 1.25rem;
        text-align: left;
        border-bottom: 2px solid #e5e5e7;
        position: sticky;
        top: 0;
        z-index: 10;
    }

    .result-section table td {
        padding: 1rem 1.25rem;
        border-bottom: 1px solid #f5f5f7;
        color: #1d1d1f;
        transition: all 0.2s ease-in-out;
    }

    .result-section table tr:last-child td {
        border-bottom: none;
    }

    .result-section table tbody tr {
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .result-section table tbody tr:hover {
        background-color: #f9f9fb;
        transform: scale(1.005);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    }

    .result-section table tbody tr:hover td {
        color: #000000;
    }
    
    /* Expander 动画效果 */
    .stExpander {
        animation: fadeIn 1s ease-out 0.6s both;
    }

    /* 结果区域入场动画 */
    .result-section {
        animation: fadeInUp 1s cubic-bezier(0.16, 1, 0.3, 1) 0.2s both;
    }

    /* 成功/警告/错误消息样式 - 增强视觉效果 */
    .stSuccess {
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 1.5px solid #bae6fd;
        animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .stWarning {
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 1.5px solid #fde68a;
        animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .stError {
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 1.5px solid #fecaca;
        animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    /* 下载按钮样式 - Apple风格 */
    .stDownloadButton > button {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Helvetica, Inter, Arial, sans-serif;
        font-size: 0.875rem;
        font-weight: 500;
        background-color: #f5f5f7;
        color: #1d1d1f;
        border: 1.5px solid #e5e5e7;
        border-radius: 16px;
        padding: 0.625rem 1.25rem;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
    }

    .stDownloadButton > button:hover {
        background-color: #e8e8ed;
        border-color: #c7c7cc;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    .stDownloadButton > button:active {
        transform: translateY(0);
    }
    
    /* 分割线样式 */
    .stDivider {
        margin: 2rem 0;
        border-top: 1px solid #d2d2d7;
    }
    
    /* 加载动画 - 更精致的样式 */
    .stSpinner {
        margin: 2rem 0;
    }

    .stSpinner > div {
        border-color: #e5e5e7 !important;
        border-top-color: #1d1d1f !important;
        animation: spin 0.8s cubic-bezier(0.16, 1, 0.3, 1) infinite;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
    
    /* 移除可能的空白容器 */
    .main .block-container > div:empty {
        display: none;
    }
    
    /* 响应式设计 - 优化移动端体验 */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
            letter-spacing: -0.01em;
        }

        .subtitle {
            font-size: 1rem;
        }

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .main-stage-card {
            padding: 2rem 1.5rem;
            border-radius: 20px;
        }

        .stRadio [role="radiogroup"] > label {
            font-size: 0.8125rem;
            padding: 0.5rem 1rem;
        }

        .stButton > button {
            min-width: 180px;
            padding: 0.75rem 2rem;
            font-size: 0.9375rem;
        }

        .result-section table {
            font-size: 0.8125rem;
        }

        .result-section table th,
        .result-section table td {
            padding: 0.75rem 1rem;
        }
    }

    @media (max-width: 480px) {
        .main-title {
            font-size: 2rem;
        }

        .stRadio [role="radiogroup"] {
            flex-direction: column;
            align-items: stretch;
        }

        .stRadio [role="radiogroup"] > label {
            width: 100%;
            text-align: center;
        }
    }

    /* 滚动条样式 - Apple风格 */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: transparent;
    }

    ::-webkit-scrollbar-thumb {
        background: #d2d2d7;
        border-radius: 10px;
        border: 2px solid transparent;
        background-clip: padding-box;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #a1a1a6;
        border-radius: 10px;
        border: 2px solid transparent;
        background-clip: padding-box;
    }

    /* 平滑滚动 */
    html {
        scroll-behavior: smooth;
    }

    /* 文字选择颜色 */
    ::selection {
        background: rgba(0, 0, 0, 0.1);
        color: inherit;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # 主标题（在卡片外）
    st.markdown('<h1 class="main-title">用户声音洞察</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">VOC Insights</p>', unsafe_allow_html=True)
    
    # 顶部信息 Expander（在卡片外）
    with st.expander("📖 使用说明与分类标准", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 使用说明
            
            1. 在下方文本框中输入或粘贴用户评论（每行一条）
            2. 点击"生成分析报告"按钮
            3. 查看分析结果和统计报告
            4. 可选择下载 Markdown 格式的报告
            
            ### 分类标准
            
            - **1-功能稳定性**：闪退、卡顿、无法播放、下载失败、网络连接错误
            - **2-交互与体验UI/UX**：界面、按钮、操作、字体、夜间模式等
            - **3-商业化**：会员价格、广告弹窗、数字专辑购买、自动扣费
            - **4-内容版权**：歌曲变灰、版权少、音质差、曲库不全
            - **5-其他**：纯情绪宣泄、无意义乱码、好评、非产品相关内容
            """)
        
        with col2:
            st.markdown("""
            ### 情感打分标准
            
            - **1分（愤怒）**：包含脏话、威胁卸载、极度失望
            - **2分（不满）**：提出批评，语气较重，但还在讲道理
            - **3分（中立）**：提出建议，或者陈述事实，无明显情绪
            - **4分（满意）**：认可产品，但有小建议
            - **5分（惊喜）**：纯夸奖，非常喜欢
            
            ### 紧迫度标准
            
            - **P0（高危）**：涉及崩溃、无法使用、资损（钱扣了没到账）
            - **P1（重要）**：体验差，但不影响核心功能使用
            - **P2（一般）**：视觉建议或新功能请求
            """)
    
    # Main Stage 卡片容器 - 使用CSS类创建视觉分组
    st.markdown('<div class="main-stage-card">', unsafe_allow_html=True)
    
    # 输入方式选择
    input_method = st.radio(
        "",
        ["直接输入", "示例数据"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # 输入框
    if input_method == "示例数据":
        sample_comments = """昨天更新后应用一直闪退，根本用不了！
界面设计太难看了，按钮也找不到
会员价格太贵了，能不能便宜点
很多歌曲都变灰了，版权太少了
希望能添加夜间模式，晚上用着太亮了
不错的产品，就是广告有点多
太棒了！非常喜欢这个应用！
充值后钱扣了但VIP没到账！
应用卡顿严重，体验很差
希望能优化一下界面设计"""
        comments_text = st.text_area(
            "",
            value=sample_comments,
            height=300,
            label_visibility="collapsed",
            placeholder="在此粘贴用户评论，AI 将自动分析情感与痛点..."
        )
    else:
        comments_text = st.text_area(
            "",
            height=300,
            label_visibility="collapsed",
            placeholder="在此粘贴用户评论，AI 将自动分析情感与痛点..."
        )
    
    # 按钮容器（居中）
    _, col2, _ = st.columns([1, 1, 1])
    with col2:
        analyze_button = st.button(
            "✨ 生成分析报告",
            type="primary",
            use_container_width=True
        )
    
    # 关闭卡片容器
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 执行分析
    if analyze_button:
        if not comments_text.strip():
            st.warning("⚠️ 请输入至少一条评论！")
        else:
            # 解析评论列表
            comments = [line.strip() for line in comments_text.strip().split('\n') if line.strip()]
            
            if not comments:
                st.warning("⚠️ 没有找到有效的评论！")
            else:
                with st.spinner(f'正在分析 {len(comments)} 条评论...'):
                    try:
                        # 创建分析器并分析
                        analyzer = CommentAnalyzer()
                        analyzer.add_comments(comments)
                        report = analyzer.generate_report()
                        
                        # 显示统计信息
                        st.success(f"✅ 成功分析 {len(comments)} 条评论！")
                        
                        # 结果区域
                        st.markdown('<div class="result-section">', unsafe_allow_html=True)
                        
                        # 分隔线
                        st.divider()
                        
                        # 解析报告（分为两个表格）
                        parts = report.split('\n---\n')
                        
                        if len(parts) >= 2:
                            # 核心数据汇总表
                            st.markdown('### 📈 核心数据汇总表')
                            st.markdown(parts[0])
                            
                            st.divider()
                            
                            # 全量评论分析明细表
                            st.markdown('### 📋 全量评论分析明细表')
                            st.markdown(parts[1])
                        else:
                            # 如果格式不对，直接显示完整报告
                            st.markdown(report)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # 添加下载按钮
                        st.divider()
                        st.download_button(
                            label="📥 下载分析报告 (Markdown格式)",
                            data=report,
                            file_name="comment_analysis_report.md",
                            mime="text/markdown"
                        )
                        
                    except Exception as e:
                        st.error(f"❌ 分析过程中出现错误：{str(e)}")
                        st.exception(e)


if __name__ == "__main__":
    main()
