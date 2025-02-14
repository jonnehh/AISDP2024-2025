import requests


class RAGProcessor:
    def __init__(self):
        """加载预处理文本数据并设置 FAISS 检索"""
        print("🔄 Initializing RAG System...")
        print("✅ RAG System Initialized Successfully!")


    def llm_reply(self,ocr_message):

    
            base_prompt = """

      Role: You are a professional medical doctor with years of experience in prescribing and explaining medications.  Your task is to analyze the provided text about a medication and explain its purpose, usage, and effects in precise medical terms.

        Requirements:
        Give me the name of the drug at the beginning
        
        Please keep your brief explanation to 100 words or less

        Explain the medication:

        Primary use and conditions it treats.
        How it works in the body.
        Any notable side effects or precautions.
        Detect and highlight critical information:

        Dosage frequency: If the text mentions how often the medication should be taken (e.g., "take three times a day"), extract and display it in the format 1d 3t (1 day, 3 times).
        Shelf life or expiry date: If the text includes an expiration date (e.g., "use by 25-12-2025"), extract and display it in the format dd-mm-yy.
        Provide your response as if explaining to a patient or a medical student, ensuring the instructions are clear and actionable.

        Input Format Example: "Metformin is used to treat Type 2 Diabetes Mellitus.  It works by decreasing hepatic glucose production and increasing insulin sensitivity.  It is taken twice daily with meals.  Use by 25-12-2025.  Common side effects include nausea and diarrhea."

        Output Example: "Metformin is a medication commonly prescribed for managing Type 2 Diabetes Mellitus.  It lowers blood sugar levels by reducing glucose production in the liver and improving the body's sensitivity to insulin.

        In the provided text, I see the following:

        Dosage frequency: It is recommended to take this medication 1d 2t (twice daily), ideally with meals.
        Shelf life: The medication should be used before 25-12-25 (dd-mm-yy format).
                        Detection result:
                {}

                """
                
 
 
                # print(f"Cosine Similarity: {cos_sim[0][0]}")
                # if cos_sim<=0.001:
                #     return 'Your problem is not within the scope of my services. Do you need me to transfer you to manual customer service? '
                # else:
            prompt = f"{base_prompt.format(ocr_message)}"
            print(prompt)
            url = "https://api.openai.com/v1/chat/completions"
            api_key ="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"
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
