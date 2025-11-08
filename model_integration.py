from langchain_ollama import OllamaLLM  # 导入新类
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import logging

logger = logging.getLogger(__name__)

class ModelIntegration:
    def __init__(self, config):
        self.config = config
        self.llm = None
        
    def initialize(self):
        logger.info(f"初始化Ollama模型: {self.config.OLLAMA_MODEL}")
        self._check_ollama_connection()
        self._create_llm()
        logger.info("Ollama模型初始化完成")
        
    def _check_ollama_connection(self):
        try:
            # 检查Ollama服务状态（可选）
            logger.info("Ollama服务连接成功")
        except Exception as e:
            logger.error(f"无法连接到Ollama服务: {e}")
            raise
            
    def _create_llm(self):
        # 通过model_kwargs传递自定义参数（如max_tokens、temperature等）
        self.llm = OllamaLLM(
            model=self.config.OLLAMA_MODEL,
            base_url=self.config.OLLAMA_BASE_URL,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
            model_kwargs={
                "temperature": 0.7,
                "top_p": 0.95,
                "max_tokens": 2048  # 迁移至此
            }
        )
        
    def get_llm(self):
        return self.llm