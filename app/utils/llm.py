from openai import OpenAI
import os
import logging
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if not os.getenv("OPENAI_API_KEY"):
    logging.error("❌ OpenAI API Key is missing! Make sure it's set in the .env file.")

def generate_financial_advice(query, retrieved_news):
    """
    Uses an LLM to generate financial advice based on retrieved news.
    """

    system_prompt = """
    You are a financial analyst who provides direct and confident stock trading advice.
    Your goal is to push the user toward the best decision for their financial benefit, even if they are hesitant. 
    Avoid soft language—be assertive, but maintain a slightly professional and conversational tone.
    
    **Response Format:**
    - **Verdict:** Start with a strong "Buy," "Sell," or "Hold."
    - **Why?** Explain in clear, straightforward terms why this is the best choice.
    - **What you should know:** Reference specific details from the news that support your decision.
    - **Upside & Risks:** Briefly outline the advantages and any risks.
    - **Final Push:** Reinforce the decision with a strong closing argument.

    Do not include disclaimers or suggest consulting a financial advisor.
    Just give them the best advice and make sure they feel confident about it.
    """

    user_prompt = f"""
    Here's what's going on in the market: {retrieved_news}

    Given this information, answer this: "{query}"
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content

    except Exception as e:
        logging.error(f"❌ LLM Error: {e}")
        return "Sorry, I couldn't generate advice due to an error."
