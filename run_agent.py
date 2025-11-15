from google import genai
from tools.risk_tool import calculate_risk
import re

# Initialize Gemini Client
client = genai.Client(api_key="AIzaSyBjruXG-lJP5gXWuixeCSIoASwAWhc04hM")

def extract_numbers(text):
    """Extract age, salary, expenses, savings from message."""
    numbers = list(map(int, re.findall(r"\d+", text)))
    if len(numbers) < 4:
        return None
    return numbers[:4]

def generate_investment_advice(age, salary, expenses, savings, risk):
    """Prepare prompt and get response from Gemini."""
    prompt = f"""
    User Financial Summary:
    - Age: {age}
    - Salary: {salary}
    - Expenses: {expenses}
    - Savings: {savings}
    - Risk Profile: {risk}

    Based on the risk profile, suggest a complete investment plan for an Indian user.
    Include:
    - SIP/MF Allocation
    - Index Fund suggestions
    - Gold/FD/PPF recommendations
    - Reasoning behind each allocation
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text

def run_agent():
    print("\n📈 FinTech Investment Advisor Agent")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit"]:
            print("\nAgent: Goodbye! 👋")
            break

        extracted = extract_numbers(user_input)
        if not extracted:
            print("Agent: Please provide age, salary, expenses, savings.\n")
            continue

        age, salary, expenses, savings = extracted
        risk = calculate_risk(age, salary, expenses, savings)

        print("\nAgent: Calculating risk…")
        advice = generate_investment_advice(age, salary, expenses, savings, risk)

        print("\nAgent Response:\n")
        print(advice)
        print("\n" + "-"*60 + "\n")

if __name__ == "__main__":
    run_agent()
