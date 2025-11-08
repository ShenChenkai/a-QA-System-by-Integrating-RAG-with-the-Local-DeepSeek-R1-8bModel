from langchain_community.vectorstores import Chroma  # 修正导入
from langchain_community.embeddings import HuggingFaceEmbeddings  # 修正导入
import os
import logging

logger = logging.getLogger(__name__)

class VectorDB:
    def __init__(self, config):
        self.config = config
        self.embeddings = None
        self.vectorstore = None
        
    def initialize(self, documents):  # 接收Document对象列表
        logger.info("初始化向量数据库")
        self._create_embeddings()
        
        if self._db_exists():
            logger.info("加载现有向量数据库")
            self._load_existing_db()
        else:
            logger.info("创建新的向量数据库")
            self.vectorstore = Chroma.from_documents(
                documents=documents,  # 直接传入Document对象
                embedding=self.embeddings,
                persist_directory=self.config.VECTOR_DB_DIR
            )
            self.vectorstore.persist()
        
        logger.info("向量数据库初始化完成")
            
    def _create_embeddings(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.config.EMBEDDING_MODEL,
            model_kwargs={"device": "cuda" if self._check_cuda() else "cpu"}
        )
        
    def _db_exists(self):
        return os.path.exists(self.config.VECTOR_DB_DIR) and os.listdir(self.config.VECTOR_DB_DIR)
    
    def _load_existing_db(self):
        self.vectorstore = Chroma(
            embedding_function=self.embeddings,
            persist_directory=self.config.VECTOR_DB_DIR
        )
        
    def get_retriever(self):
        return self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": self.config.RETRIEVAL_K}
        )
        
    def _check_cuda(self):
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False