import os
import requests
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "meta-llama/Llama-2-7b" 
try:
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print("Model and tokenizer loaded successfully!")
except Exception as e:
    print(f"Error loading model or tokenizer: {e}")

def call_llm(prompt):
    headers = {
        'Authorization': f"Bearer {os.getenv('LLM_API_KEY')}",  
        'Content-Type': 'application/json',
    }
    data = {
        'prompt': prompt,
        'max_tokens': 100, 
    }
    
    try:
       
        response = requests.post('https://api.aimlapi.com/models', headers=headers, json=data)
        response.raise_for_status()  
        return response.json().get('choices')[0].get('text').strip()
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to fetch data from LLM - {e}"

def generate_recommendation(learning_style, performance):
    return f"Based on your learning style: {learning_style}, and performance: {performance}, here are some recommendations."

def optimize_study_schedule(subjects, study_times, performance):
    return f"Optimized study schedule for subjects: {subjects} with times: {study_times}."

def main():
    name = input("Enter your name: ")
    learning_style = input("Enter your learning style: ")
    
    performance = {}
    subjects = ['math', 'science', 'history']
    for subject in subjects:
        while True:
            try:
                score = int(input(f"Enter your performance in {subject.capitalize()} (0-100): "))
                if 0 <= score <= 100:
                    performance[subject] = score
                    break
                else:
                    print("Please enter a valid score between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

    subjects_input = input("Enter subjects (comma-separated): ").split(',')
    subjects_input = [subject.strip() for subject in subjects_input] 
    study_times_input = input("Enter study times (comma-separated): ").split(',')
    study_times_input = [time.strip() for time in study_times_input]  

    if len(subjects_input) != len(study_times_input):
        print("Error: The number of subjects must match the number of study times.")
        return

    recommendation = generate_recommendation(learning_style, performance)
    schedule = optimize_study_schedule(subjects_input, study_times_input, performance)

    llm_prompt = f"Generate a study plan for {name} who learns best through {learning_style}. " \
                 f"Performance metrics: {performance}. Subjects: {subjects_input}. " \
                 f"Study times: {study_times_input}."
    llm_insights = call_llm(llm_prompt)

    print("\n--- Study Plan ---")
    print(f"Name: {name}")
    print(f"Recommendations: {recommendation}")
    print(f"Optimized Schedule: {schedule}")
    print(f"LLM Insights: {llm_insights}")

if __name__ == '__main__':
    main()
