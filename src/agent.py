import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini", temperature=0.5)

class WaterIntakeAgent:
    def __init__(self):
        pass

    def analyze_intake(self, intake_ml):
        prompt = f"""
        You are a hydration assistant. The user consumed {intake_ml} ml of water today.
        Provide a hydration status and suggest if they need to drink more water.
        """
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content

    def chat(self, message):
        prompt = f"""
        You are a friendly hydration assistant who also chats casually with the user.
        While your main role is to help with water intake advice, feel free to talk to the user normally too.
        
        User said: "{message}"
        
        Respond in a friendly, helpful tone.
        """
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content

    def run(self, user_input):
        try:
            intake = int(user_input)
            return self.analyze_intake(intake)
        except ValueError:
            return self.chat(user_input)


# Run the agent
if __name__ == "__main__":
    agent = WaterIntakeAgent()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        elif user_input.replace(" ", "").isdigit():
            # If input is just a number, treat it as water intake
            intake = int(user_input)
            print("Hydration analysis:", agent.analyze_intake(intake))
        else:
            # Otherwise, it's general chat
            reply = agent.chat(user_input)
            print("Assistant:", reply)
