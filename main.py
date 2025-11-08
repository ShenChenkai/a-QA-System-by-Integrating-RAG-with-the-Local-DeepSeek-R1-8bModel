import sys
from pathlib import Path
from config import Config
from document_processor import DocumentProcessor
from vector_db import VectorDB
from model_integration import ModelIntegration
from rag_chain import RAGChain
from utils import setup_logging, format_response
import logging
from fastapi import FastAPI, Request
import uvicorn
from utils import format_response
from pydantic import BaseModel  # 新增导入
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# 定义请求体模型
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发阶段允许所有域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str
rag_chain_instance = None  # 全局RAG链实例

@app.on_event("startup")
async def startup_event():
    """初始化RAG链（与现有逻辑一致）"""
    global rag_chain_instance
    setup_logging(Config.LOG_LEVEL)
    doc_processor = DocumentProcessor(Config)
    documents = doc_processor.process_pdf_directory()
    vector_db = VectorDB(Config)
    vector_db.initialize(documents)
    model = ModelIntegration(Config)
    model.initialize()
    rag_chain_instance = RAGChain(Config, model.get_llm(), vector_db.get_retriever())
    rag_chain_instance.initialize()

@app.post("/api/rag-query")
async def rag_query(request: QueryRequest):  # 修改参数类型
    """处理前端查询请求"""
    query = request.query  # 从模型中获取query字段
    result = rag_chain_instance.run_query(query)
    return format_response(result)

if __name__ == "__main__":
    # 启动FastAPI服务（需与Streamlit分开运行）
    uvicorn.run(app, host="0.0.0.0", port=8000)


def main():
    setup_logging(Config.LOG_LEVEL)
    logger = logging.getLogger(__name__)
    
    try:
        # 添加项目根目录到Python路径
        project_root = str(Path(__file__).parent)
        sys.path.append(project_root)
        
        # 初始化模块
        doc_processor = DocumentProcessor(Config)
        documents = doc_processor.process_pdf_directory()
        
        vector_db = VectorDB(Config)
        vector_db.initialize(documents)
        retriever = vector_db.get_retriever()
        
        model = ModelIntegration(Config)
        model.initialize()
        llm = model.get_llm()
        
        rag_chain = RAGChain(Config, llm, retriever)
        rag_chain.initialize()
        
        # 交互式查询（可取消注释以启用）
        while True:
            user_query = input("\n请输入问题（输入'退出'结束）: ")
            if user_query.lower() in ["退出", "q"]:
                break
            result = rag_chain.run_query(user_query)
            print(format_response(result))
        
        # 示例查询（自动执行）
        ##logger.info(f"执行示例查询: {sample_query}")
        #result = rag_chain.run_query(sample_query)
        #formatted_result = format_response(result)
        
        # 打印结果
       # print("\n" + "="*50)
       # print(f"问题: {formatted_result['question']}")
       # print("\n回答:")
       # print(formatted_result['answer'])
        
        print("\n" + "-"*50)
        print("引用文档:")
        for i, doc in enumerate(format_response["source_documents"]) :
            print(f"\n来源文档 {i+1} ({doc['metadata']['source']}):")
            print(doc["content"])
        
        print("\n" + "="*50)
        
    except Exception as e:
        logger.error(f"程序运行出错: {e}", exc_info=True)
        print(f"错误: {e}")

if __name__ == "__main__":
    main()