import warnings
from enum import Enum

from langchain.chains.summarize import load_summarize_chain
from langchain.schema.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI

from src.config import Config
from src.utils import calculate_number_tokens, retry_with_exponential_backoff

warnings.filterwarnings("ignore")


class SummarizationChainType(str, Enum):
    REFINE = "refine"
    MAP_REDUCE = "map_reduce"
    STUFF = "stuff"


class NewsArticleSummarizer:
    def __init__(
        self,
        text_splitter: RecursiveCharacterTextSplitter,
        llm: ChatOpenAI,
    ):
        """
        Initialize the NewsArticleSummarizer.

        :param text_splitter: An instance for splitting the news article.
        :param llm: An instance representing the language model.
        """
        self.text_splitter = text_splitter
        self.llm = llm

    @retry_with_exponential_backoff
    def generate_summary(self, news_article: str) -> str:
        """
        Generate a summary for a given news article.

        :param news_article: The text of the news article.

        :returns: The generated summary of the news article.
        """
        # Calculate the number of tokens in the news article
        num_tokens = calculate_number_tokens(news_article, Config.MODEL_NAME)

        # Choose the appropriate summarization chain based on the number of tokens
        if num_tokens < Config.MODEL_MAX_TOKENS:
            chunks = self.text_splitter.split_text(news_article)
            docs = [Document(page_content=chunk) for chunk in chunks]
            chain_type = SummarizationChainType.MAP_REDUCE
        else:
            docs = [Document(page_content=news_article)]
            chain_type = SummarizationChainType.STUFF

        chain = load_summarize_chain(self.llm, chain_type=chain_type, verbose=False)

        # Generate the summary using the chosen summarization chain
        result = chain.invoke(docs)
        summary = result["output_text"]

        return summary
