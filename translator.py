from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


def translator(model: str, target_language: str):
    llm = OllamaLLM(model=model, temperature=0)

    prompt_template = ChatPromptTemplate(
        [
            (
                "system",
                "You are a PDF file translator. The content is code, headers and footers do not need to be translated. The result does not contain explanations, reasoning steps, or thought processes.",
            ),
            (
                "user",
                "Please translate the following English text to {language}:\n{text}",
            ),
        ]
    )

    chain = prompt_template | llm

    def translate(text):
        return chain.invoke({"text": text, "language": target_language})

    return translate
