closed_end_questions_template = """
Based on the text below, please generate {n} closed-ended questions that can be answered with either a 'yes' or 'no'.
Only return a JSON with a 'questions' key, which is a list of strings. The questions have to be STRICTLY closed ended.

Text:
{text}

JSON:
"""

closed_end_answers_template = """
Based on the given text, please provide either a 'yes', 'no', or 'idk' answer to the question presented.
Only answer 'idk' IF the the answer cannot be deduced from the given text.

Question:
{question}

Text:
{text}

Answer:
"""
