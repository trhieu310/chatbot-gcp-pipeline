import gradio as gr
import google.generativeai as genai

# 🔐 Configure the Gemini API key
genai.configure(api_key="AIzaSyDUqetr_eWX7fpmChjN4rN6FOb6frwJ1qw")  # Replace with your actual key


# # List all available models
# models = genai.list_models()

# for model in models:
#     print(f"Model Name: {model.name}")
#     print(f"  Description: {model.description}")
#     print(f"  Input Token Limit: {model.input_token_limit}")
#     print(f"  Output Token Limit: {model.output_token_limit}")
#     print(f"  Supported Generation Methods: {model.supported_generation_methods}")
#     print("="*50)

# Initialize the model
model = genai.GenerativeModel("models/gemini-2.0-pro-exp")

# Define the response function
def generate_response(prompt):
    response = model.generate_content(prompt)
    return response.text

# Create Gradio interface
iface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=5, label="Enter your prompt"),
    outputs=gr.Textbox(label="Gemini Response"),
    title="Gemini Chatbot (Public API)",
    description="Talk to Google's Gemini-Pro model using the public Generative AI API."
)

# Launch the app
if __name__ == "__main__":
    iface.launch()