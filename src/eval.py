import json
from concurrent.futures import ThreadPoolExecutor
from enum import Enum

from langchain_openai import ChatOpenAI

from src.template import closed_end_answers_template, closed_end_questions_template


class QuestionSource(str, Enum):
    ORIGINAL = "original"
    GENERATED = "generated"


class EvalSummarizer:
    def __init__(self, llm: ChatOpenAI):
        """Initialize the EvalSummarizer instance."""
        self.llm = llm

    def answer_question(self, prompt: str) -> str:
        """Get the model's answer to a given prompt."""
        answer = self.llm.invoke(prompt).content
        return answer

    def generate_questions(self, text: str, number_questions: int) -> list[str]:
        """Generate a list of questions."""
        prompt = closed_end_questions_template.format(n=number_questions, text=text)
        result = self.answer_question(prompt)
        result_dict = json.loads(result)
        questions = result_dict["questions"]
        return questions

    def calculate_score(
        self,
        question_source: QuestionSource,
        number_questions: int = 5,
        original_text: str = None,
        generated_text: str = None,
    ) -> float:
        """Calculate the evaluation score based on both answers."""
        score = 0

        if question_source == QuestionSource.ORIGINAL:
            questions = self.generate_questions(original_text, number_questions)
        else:
            questions = self.generate_questions(generated_text, number_questions)

        for question in questions:
            prompt_original = closed_end_answers_template.format(
                question=question, text=original_text
            )
            prompt_summary = closed_end_answers_template.format(
                question=question, text=generated_text
            )

            answer_original_text = self.answer_question(prompt_original)
            answer_summary = self.answer_question(prompt_summary)

            score += (
                answer_original_text.strip().lower() == answer_summary.strip().lower()
            )

        score = score / len(questions)
        return score

    def evaluate_summary(
        self,
        number_questions: int = 5,
        original_text: str = None,
        generated_text: str = None,
    ) -> float:
        """Evaluate the summary based on questions from original text or generated text"""

        with ThreadPoolExecutor() as executor:
            future_score_original = executor.submit(
                self.calculate_score,
                QuestionSource.ORIGINAL,
                number_questions,
                original_text,
                generated_text,
            )
            future_score_generated = executor.submit(
                self.calculate_score,
                QuestionSource.GENERATED,
                number_questions,
                original_text,
                generated_text,
            )

            score_orginal = future_score_original.result()
            score_generated = future_score_generated.result()

        score = min(score_orginal, score_generated)
        return score
