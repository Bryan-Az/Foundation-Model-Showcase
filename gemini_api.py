import os
import google.generativeai as genai
from typing import Dict, Any, Optional
import PyPDF2
import io

def process_pdf(pdf_file: io.BytesIO) -> str:
    """
    Process a PDF file and extract its text content.

    Args:
    pdf_file (io.BytesIO): The PDF file as a BytesIO object.

    Returns:
    str: The extracted text content from the PDF.
    """
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text_content = []
    for page in pdf_reader.pages:
        text_content.append(page.extract_text())
    return "\n".join(text_content)

def call_gemini_api(prompt: Optional[str] = None, pdf_file: Optional[io.BytesIO] = None, model: str = "gemini-pro") -> Dict[str, Any]:
    """
    Call the Gemini API with a given prompt or PDF file content.

    Args:
    prompt (Optional[str]): The input prompt for the Gemini model. Defaults to None.
    pdf_file (Optional[io.BytesIO]): The PDF file as a BytesIO object. Defaults to None.
    model (str): The Gemini model to use. Defaults to "gemini-pro".

    Returns:
    Dict[str, Any]: A dictionary containing the API response.

    Raises:
    ValueError: If the API key is not set, neither prompt nor pdf_file is provided, or the API call fails.
    """
    # Check if the API key is set
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")

    if prompt is None and pdf_file is None:
        raise ValueError("Either prompt or pdf_file must be provided")

    try:
        # Configure the Gemini API
        genai.configure(api_key=api_key)

        # Set up the model
        model = genai.GenerativeModel(model)

        # Process input
        if pdf_file:
            content = process_pdf(pdf_file)
        else:
            content = prompt

        # Generate content
        response = model.generate_content(content)

        # Return the response as a dictionary
        return {
            "generated_text": response.text,
            "safety_ratings": [
                {
                    "category": rating.category,
                    "probability": rating.probability
                } for rating in response.prompt_feedback.safety_ratings
            ],
            "model": model.model_name,
        }

    except Exception as e:
        raise ValueError(f"Error calling Gemini API: {str(e)}")

# Example usage
if __name__ == "__main__":
    try:
        # Example with string prompt
        result = call_gemini_api(prompt="Tell me a short joke about programming.")
        print("Result from string prompt:")
        print(result["generated_text"])

        # Example with PDF file
        with open("example.pdf", "rb") as pdf_file:
            pdf_bytes = io.BytesIO(pdf_file.read())
            result = call_gemini_api(pdf_file=pdf_bytes)
            print("\nResult from PDF file:")
            print(result["generated_text"])
    except ValueError as e:
        print(f"Error: {str(e)}")