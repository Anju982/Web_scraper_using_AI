from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import openai
from dotenv import load_dotenv
import os

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_with_ollama(dom_chunks, parse_description):
    model = OllamaLLM(model="llama3")
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    
    pasred_results = []
    
    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke({"dom_content" : chunk, "parse_description" : parse_description})
        print(f"Parsed batch {i} of {len(dom_chunks)}")
        pasred_results.append(response)
        
    return "\n".join(pasred_results)

def pasrse_with_openai(dom_chunks, parse_description):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    parsed_results = []
    
    for i, chunk in enumerate(dom_chunks, start=1):
        prompt = template.format(dom_content=chunk, parse_description=parse_description)
        
        #Make the API call to openAI chatcompletion
        respones = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that extracts specific information from text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0  # Set to 0 for deterministic, factual output
        )
        
        #Extract the result from model
        # Extract the response from the model
        result = respones['choices'][0]['message']['content']
        print(f"Parsed batch {i} of {len(dom_chunks)}")
        parsed_results.append(result.strip())  # Append the stripped result
    
    # Join all results with a newline separator
    return "\n".join(parsed_results)