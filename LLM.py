from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
answer the question below.

Question: Provide a brief interpretation of the following tarot cards: {question}

Answer:
"""

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def interpret_tarot_cards(card_names):
    question = f"""KEEP YOUR REPLY BRIEF! 2 sentences maximum! In the tone of a fortuneteller, provide an interpretation of these 3 tarot cards: {', '.join(card_names)} . 
    These cards are being drawn to decide whether or not a particular stock is wise to invest in, decide if the cards are saying to buy or sell a particular stock.
    You must mention all 3 cards by name."""
    result = chain.invoke({"question": question})
    return result