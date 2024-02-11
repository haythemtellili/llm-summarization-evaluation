from fastapi import FastAPI, HTTPException

from src.models import SummaryRequest, SummaryResponse
from src.main import initialize_components, initialize_openai

app = FastAPI()

# Initialize OpenAI and summarizer, evaluator
initialize_openai()
summarizer, evaluator = initialize_components()


@app.post("/summarize", response_model=SummaryResponse, tags=["Summarization"])
async def summarize_text(request: SummaryRequest):
    """
    Endpoint to generate a summary for a given text.

    Parameters:
        - request: SummaryRequest model containing the text to be summarized.

    Returns:
        - A SummaryResponse model containing the generated summary.
    """
    try:
        summary = summarizer.generate_summary(request.text)
        score = evaluator.evaluate_summary(5, request.text, summary)
        return {"summary": summary, "score": score}

    except Exception as e:
        # Log the error for debugging purposes
        app.logger.error(f"Error occurred during summarization: {str(e)}")

        # Raise an HTTPException with a 500 Internal Server Error status
        raise HTTPException(status_code=500, detail="Internal Server Error")
