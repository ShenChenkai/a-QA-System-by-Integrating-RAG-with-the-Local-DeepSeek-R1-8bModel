import streamlit as st
import requests
from config import Config
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

# 配置后端API地址
API_URL = f"{Config.BACKEND_BASE_URL}/api/rag-query"

def main():
    # 设置页面配置
    st.set_page_config(
        page_title="RAG知识库问答系统",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 自定义CSS样式
    st.markdown("""
    <style>
    /* 全局样式 */
    body {
        font-family: 'Inter', sans-serif;
        background-color: #f8fafc;
    }
    
    /* 标题样式 */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e40af;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 副标题样式 */
    .sub-title {
        font-size: 1.2rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* 卡片容器样式 */
    .card {
        background-color: white;
        border-radius: 0.75rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    /* 输入框样式 */
    .input-field {
        width: 100%;
        padding: 0.75rem 1rem;
        border: 1px solid #cbd5e1;
        border-radius: 0.5rem;
        font-size: 1rem;
        transition: all 0.2s ease;
    }
    
    .input-field:focus {
        outline: none;
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
    }
    
    /* 按钮样式 */
    .submit-button {
        background-color: #3b82f6;
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .submit-button:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
    }
    
    .submit-button:active {
        transform: translateY(1px);
    }
    
    /* 结果标题样式 */
    .result-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e40af;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    /* 来源文档样式 */
    .source-document {
        background-color: #f1f5f9;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .source-title {
        font-weight: 600;
        color: #334155;
        margin-bottom: 0.5rem;
    }
    
    /* 加载动画 */
    .loader {
        border: 4px solid rgba(0, 0, 0, 0.1);
        border-left-color: #3b82f6;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .sub-title {
            font-size: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 页面标题和描述
    st.markdown('<h1 class="main-title">📚 浙江大学校园信息问答系统</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">基于Ollama和LangChain构建的本地deepseek问答系统</p>', unsafe_allow_html=True)
    
    # 侧边栏说明
    with st.sidebar:
        st.markdown("## 📖 使用指南")
        st.markdown("1. 在输入框中输入您的问题")
        st.markdown("2. 点击提交按钮获取回答")
        st.markdown("3. 系统会从知识库中检索相关信息并生成回答")
        st.markdown("4. 回答下方会显示引用的源文档片段")
        
        st.markdown("## ⚙️ 系统信息")
        st.markdown(f"- 后端模型: {Config.OLLAMA_MODEL}")
        st.markdown(f"- 知识库: {len(Config.DOCUMENT_PATHS)}个PDF文档")
        
        st.markdown("## 📝 注意事项")
        st.markdown("- 请保持问题简洁明了")
        st.markdown("- 复杂问题可能需要更长的处理时间")
        st.markdown("- 系统回答仅供参考，不代表专业意见")
    
    # 主内容区
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col2:
        # 输入卡片
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            st.markdown("### 💬 请输入您的问题")
            user_question = st.text_area(
                "", 
                height=100, 
                placeholder="例如：浙江大学本科辅修的申请条件是什么？",
                key="question_input"
            )
            
            if st.button("提交查询", key="submit_button", type="primary"):
                if not user_question.strip():
                    st.warning("请输入问题")
                else:
                    with st.spinner("🔍 正在检索知识库..."):
                        try:
                            # 调用后端API（增加超时时间到60秒）
                            response = requests.post(
                                API_URL,
                                json={"query": user_question},
                                headers={"Content-Type": "application/json"},
                                timeout=60  # 增加超时时间
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                display_result(result)
                            else:
                                st.error(f"查询失败: HTTP {response.status_code}")
                                st.write(f"错误详情: {response.text}")
                        except requests.exceptions.Timeout:
                            st.error("查询超时，请尝试简化问题或稍后再试")
                        except Exception as e:
                            st.error(f"发生错误: {str(e)}")
                            st.exception(e)
            
            st.markdown('</div>', unsafe_allow_html=True)

def display_result(result):
    """不使用Markdown渲染的结果展示函数"""
    st.write("## 📜 回答")
    
    # 处理回答内容
    answer_text = result["answer"]
    # 简单预处理：去除多余空行
    answer_text = "\n".join([line.strip() for line in answer_text.split("\n") if line.strip()])
    st.write(answer_text)
    
    # 显示引用文档
    if "source_documents" in result and len(result["source_documents"]) > 0:
        st.write("## 📚 引用文档")
        
        for i, doc in enumerate(result["source_documents"]):
            st.write(f"### 📄 来源文档 {i+1}: {doc['metadata']['source']}")
            
            # 处理文档内容
            doc_content = doc["content"]
            doc_content = "\n".join([line.strip() for line in doc_content.split("\n") if line.strip()])
            st.write(doc_content)
            
            st.write("---")  # 添加分隔线

if __name__ == "__main__":
    main()