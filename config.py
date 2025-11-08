import os
from glob import glob

class Config:
    # PDF文档路径
    PDF_DIR = r"C:\Users\guont\Desktop\ds_rag\source"  # 替换为你的PDF路径
  # 新增：自动获取所有PDF文件路径

    DOCUMENT_PATHS = glob(os.path.join(PDF_DIR, "*.pdf"))
    
    # Ollama模型配置
    OLLAMA_MODEL = "deepseek-r1:8b"
    OLLAMA_BASE_URL = "http://localhost:11434"

    # 新增：FastAPI后端服务地址
    BACKEND_BASE_URL = "http://localhost:8000"  # FastAPI服务地址
    
    # 向量数据库配置
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    VECTOR_DB_DIR = "./vector_db"
    
    # 检索配置
    RETRIEVAL_K = 3  # 返回最相关的文档数
    
    # 日志配置
    LOG_LEVEL = "INFO"