import textwrap
import logging
from datetime import datetime

def setup_logging(log_level="INFO"):
    """设置日志配置"""
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(f"rag_deepseek_{datetime.now().strftime('%Y%m%d')}.log"),
            logging.StreamHandler()
        ]
    )
    
def format_response(result):
    """格式化查询结果"""
    formatted = {
        "question": result["query"],
        "answer": textwrap.fill(result["result"], width=80),
        "source_documents": []
    }
    
    for doc in result["source_documents"]:
        formatted["source_documents"].append({
            "content": textwrap.fill(doc.page_content[:300] + "...", width=80),
            "metadata": doc.metadata
        })
        
    return formatted