import os
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models

def main():
    vertexai.init(project="proven-country-426922-g1", location="us-central1")

    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    }

    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    # Create the model for OCR formatting
    model_ocr_formatter = GenerativeModel(
        "gemini-1.5-flash",
        system_instruction="You are an OCR formatter, user sends messy text that was a result of OCR, you clean it and return the result\nreturn only the formatted text with no additional notes, if something doesn't make sense, leave it as it is",
    )

    with open('Backend/Exam_Grading/ocr.txt', 'r', encoding='utf-8') as file:
        message = file.read()

    responses = model_ocr_formatter.generate_content(
        [message],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    response_text = ''.join([response.text for response in responses])

    with open('Backend/Exam_Grading/ocr_cleaned.txt', 'w', encoding='utf-8') as file:
        file.write(response_text)

    with open('Backend/Exam_Grading/QwAnswers.txt', 'r', encoding='utf-8') as file:
        questions_with_answers = file.read()

    # Create the model for grading
    model_grader = GenerativeModel(
        "gemini-1.5-pro-001",
        system_instruction=f"You are an exam grader, the user sends you their answers and you give them a score, the answers don't have to be exact but they should convey the same meaning.\n\n{questions_with_answers}\nreturn:\nQuestion 1, (review eg student got 2 out of 3 with function correctly), x degrees\nQuestion 2, (review), x degrees\nQuestion 3, (review), x degrees\nIf no answers are provided, just return error",
    )

    responses = model_grader.generate_content(
        [response_text],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    response_text = ''.join([response.text for response in responses])

    with open('Backend/Exam_Grading/grade_review.txt', 'w', encoding='utf-8') as file:
        file.write(response_text)

    # Create the model for mark formatting
    model_mark_formatter = GenerativeModel(
        "gemini-1.5-pro-001",
        system_instruction="return\nQ1: x degrees\n(review)\nQ2: x degrees\n(review)\nQ3: x degrees\n(review)\n....\nin this format\nif the user didn't send any questions or answers, just return \"error\"",
    )

    responses = model_mark_formatter.generate_content(
        [response_text],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    response_text = ''.join([response.text for response in responses])

    with open('Backend/Exam_Grading/grades.txt', 'w', encoding='utf-8') as file:
        file.write(response_text)

if __name__ == "__main__":
    main()