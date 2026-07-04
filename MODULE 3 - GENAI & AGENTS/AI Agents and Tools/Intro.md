# AI Agents and Tools
- Before going into Agents, we need to know what is an LLM and how it becomes an Agent.
- So, LLM's are like the brain where we give a question and it responds with an answer. Eg: "What is the capital of India?" and it responds with "New Delhi". This response is data that it has been trained on, not the real-time data. 
- If we ask "What is the temperature in Paris", it will hallucinate and give a random answer because it does not have access to real-time data. It doesn't know how to call a weather API to get the real-time data.
- So, when an LLM is connected to the real-time data, it becomes an Agent. It can call APIs, get the real-time data and respond with the correct answer. Eg: "What is the temperature in Paris" and it responds with "The temperature in Paris is 25 degree Celsius". This agent stops only when the task is accomplished.
- Our roles, as a developer, ois to map the API's to the LLM's and build the loop untill the task is accomplished. This is called Agentic AI.

## REACT PATTERN
- Reason and act. The core nature of any agent.
- **Step-1**: Thought: The agent thinks about the task and what it needs to do.
- **Step-2**: Action: The agent takes an action based on its thought.
- **Step-3**: Observation: The agent observes the result of its action and uses that information to inform its next thought and action.
- **Step-4**: Repeat: The agent repeats this process until it has accomplished its task or reached a stopping point.