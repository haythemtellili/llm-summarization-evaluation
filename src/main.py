import os

import openai
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI

from config import Config
from eval import EvalSummarizer
from summarize import NewsArticleSummarizer


def initialize_openai():
    # Load environment variables from the .env file
    load_dotenv()
    # Initialize the OpenAI API client
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key


def initialize_components():
    # Initialize the RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=100,
        length_function=len,
        separators=["\n"],
    )

    # Initialize the model
    llm = ChatOpenAI(temperature=0, model_name=Config.MODEL_NAME)

    # Initialize the NewsArticleSummarizer
    summarizer = NewsArticleSummarizer(text_splitter, llm)

    # Initialize the EvalSummarizer
    evaluator = EvalSummarizer(llm)

    return summarizer, evaluator


def main():
    initialize_openai()
    summarizer, evaluator = initialize_components()

    # Example usage
    news_article = (
        "Falcon comes in two sizes — 7 billion parameters (called Falcon-7B) and 40 billion parameters (called Falcon 40B)."
        "Each of the two sizes has two versions: (i) base, which has been pre-trained on large corpuses of text and can be fine-tuned on downstream tasks,"
        "and (ii) instruct, which has already been fine-tuned on instructions, making it, in our view,"
        "favorable for out-of-the-box chatbot and Q&A applications."
    )

    # Generate summary
    summary = summarizer.generate_summary(news_article)

    # Evaluate summary
    evaluation_score = evaluator.evaluate_summary(5, news_article, summary)

    # Display results
    print(f"Evaluation Score: {evaluation_score}")
    print("Generated Summary:")
    print(summary)


if __name__ == "__main__":
    main()
