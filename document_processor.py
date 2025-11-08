import os
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document  # 新增导入
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self, config):
        self.config = config
        
    def process_pdf_directory(self):
        """处理PDF目录中的所有文件"""
        pdf_dir = self.config.PDF_DIR
        logger.info(f"开始处理PDF目录: {pdf_dir}")
        
        all_docs = []
        
        # 遍历目录中的所有文件
        for filename in os.listdir(pdf_dir):
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(pdf_dir, filename)
                try:
                    # 处理单个PDF文件
                    docs = self._process_single_pdf(file_path, filename)
                    all_docs.extend(docs)
                    logger.info(f"成功处理文件: {filename}")
                except Exception as e:
                    logger.error(f"处理文件 {filename} 失败: {e}")
        
        logger.info(f"PDF目录处理完成，共生成 {len(all_docs)} 个文本块")
        return all_docs
    
    def _process_single_pdf(self, file_path, filename):
        """处理单个PDF文件"""
        # 提取PDF文本
        try:
            with pdfplumber.open(file_path) as pdf:
                pages = [page.extract_text() for page in pdf.pages]
            text = "\n".join(pages)
        except Exception as e:
            logger.error(f"提取PDF文本失败: {e}")
            return []
        
        # 文本分割
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "\n", "。", "！", "？", "；", " ", ""]
        )
        
        # 创建带有元数据的文档对象
        chunks = text_splitter.split_text(text)
        docs = [
            Document(
                page_content=chunk,
                metadata={"source": filename, "page": i+1}
            )
            for i, chunk in enumerate(chunks)
        ]
        
        return docs