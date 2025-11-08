from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import logging

logger = logging.getLogger(__name__)

class RAGChain:
    def __init__(self, config, llm, retriever):
        self.config = config
        self.llm = llm
        self.retriever = retriever
        self.chain = None
        
    def initialize(self):
        """初始化RAG链"""
        logger.info("初始化RAG链")
        prompt = self._create_prompt()
        self._create_chain(prompt)
        logger.info("RAG链初始化完成")
        
    def _create_prompt(self):
        """创建提示模板"""
        template = """
        基于以下提供的上下文信息，回答用户的问题。
        如果上下文中没有足够的信息，请说明"根据提供的文档无法回答此问题"。
        
        上下文信息:
        {context}
        
        用户问题:
        {question}
        
        回答:
        """
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
    def _create_chain(self, prompt):
        """创建RAG链"""
        self.chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )
        
    def run_query(self, query):
        """执行查询"""
        return self.chain.invoke({"query": query})