import requests


class RAGProcessor:
    def __init__(self):
        print("🔄 Initializing RAG System...")
        print("✅ RAG System Initialized Successfully!")


    def llm_reply(self,ocr_message):

    
            base_prompt = """

            Objective:
            Extract and summarize key details from an imperfect OCR result of a medicine box.

            Instructions:

            Identify the medicine name from the OCR text. If the text is unclear or contains errors, attempt to correct or infer the name based on context.
            Extract the main function or purpose of the medicine. If the OCR result is incomplete, reconstruct missing words using common medical knowledge.
            Summarize the medicine’s function in one concise and accurate sentence.
            Ensure the output is medically sound and easy to understand.
            Handle OCR artifacts (e.g., missing letters, incorrect spacing, or gibberish characters) and improve readability.
            The output text drug name is always first
            And give me a short description of the drug's function in 10 words or less
            OCR result:
                {}

                """
                
 
 
                # print(f"Cosine Similarity: {cos_sim[0][0]}")
                # if cos_sim<=0.001:
                #     return 'Your problem is not within the scope of my services. Do you need me to transfer you to manual customer service? '
                # else:
            prompt = f"{base_prompt.format(ocr_message)}"
            print(prompt)
            url = "https://api.openai.com/v1/chat/completions"
            api_key ="API_KEY"
            headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }

            data = {
                    "model": "gpt-4o",
                    "temperature": 0.7,
                    "messages": [
                        {
                            "role": "system",
                            "content": prompt ,
                        }

                    ],
                    "max_tokens": 200
                }

            response = requests.post(url, headers=headers, json=data)
            
            answer=response.json()['choices'][0]['message']['content']
        # except:
        #     answer="I apologize for the confusion. If you have any questions about mosquitoes or need information related to them, please feel free to ask. I'm here to help!"
            print(answer)
            return answer  
