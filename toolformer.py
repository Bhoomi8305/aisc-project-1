import requests
import re
from transformers import GPT2Tokenizer, GPT2LMHeadModel

class Toolformer:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")
        self.tokenizer.pad_token = self.tokenizer.eos_token  # Set pad_token to eos_token

    def generate_response(self, query):
        # Tokenize the input query properly
        inputs = self.tokenizer(query, return_tensors="pt", padding=True, truncation=True)
        
        # Generate a response using the GPT-2 model
        outputs = self.model.generate(
            inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_length=50,  # Limit the output length to avoid excessive output
            pad_token_id=self.tokenizer.eos_token_id,  # Ensure we use eos_token as padding
            num_return_sequences=1,
            do_sample=True,  # Allow some randomness
            temperature=0.7,  # Increase randomness to avoid repetition
            top_k=50,  # Limit the top-k choices at each step
            top_p=0.9  # Use nucleus sampling for diversity
        )
        
        # Decode the response and clean it up
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.strip()  # Remove leading/trailing spaces

        

    def decide_tool_use(self, input_text):
        """
        A simple heuristic to decide if tool use is needed.
        In this case, if the input contains numbers or math symbols.
        """
        if any(char in input_text for char in "0123456789+-*/="):
            return "calculator"
        return None

    def call_tool(self, tool, query):
        if tool == "calculator":
            response = requests.post(
                "http://127.0.0.1:5000/calculator", 
                json={"expression": query}
            )
            if response.status_code == 200:
                return response.json().get("result")
            else:
                return f"Error: {response.json().get('error')}"
        return "Unknown tool"

    def process_input(self, input_text):
        tool = self.decide_tool_use(input_text)
        if tool:
            # Extract the mathematical expression from the input
            expression = re.findall(r"[-+]?\d*\.\d+|\d+|[-+*/=()]", input_text)  # Find numbers and operators
            if expression:
                expression_str = " ".join(expression)  # Join numbers/operators into a valid string
                tool_result = self.call_tool(tool, expression_str)
                return f"Tool result: {tool_result}"
            else:
                return "No valid mathematical expression found."
        else:
            # If not a math query, pass to GPT-2 to generate a response (e.g., joke)
            return self.generate_response(input_text)
