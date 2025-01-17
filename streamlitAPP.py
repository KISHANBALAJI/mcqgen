import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback # type: ignore
from src.mcqgenerator.MCCQgenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

#loading json file
with open("C:\\Users\\kisha\\mcqgen\\Response.json",'r')as file:
    RESPONSE_JSON = json.load(file)

#creating a title for the app
st.title("MCQs Creator Application with LangChain")

#create a form using st.form

with st.form("user_inputs"):
    #file Upload
    uploaded_file=st.file_uploader("Upload a PDF or txt file")

    #Input files
    mcq_count = st.number_input("No.of MCQs",min_value=3,max_value=50)

    #subject
    subject=st.text_input("Insert Subject",max_chars=20)

    #Quiz Tone
    tone = st.text_input("Complexity level of Questions",max_chars=20,placeholder="simple")

    #add button
    button=st.form_submit_button("Create MCQs")
    #check if the button is cliked  and all fields have imput

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = read_file(uploaded_file)
                #Count tokens and the cost of API call
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                            "text":text,
                            "number": mcq_count,
                            "sublect":subject,
                            "tone":tone,
                            "response_json":json.dumps(RESPONSE_JSON)
                        }
                    )
                #str.write(response)
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")
            
            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens Tokens:{cb.Completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                if isinstance(response,dict):
                    #Exctract the Quiz data from the response
                    quiz=response.get("quiz",None)
                    if quiz is not None:
                        table_data=get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index+1
                            st.table(df)
                            #Display the review in atext box as well
                            st.text_area(lable="Review",value=response["review"])
                        else:
                            st.error("Error in the table data")
                    
                    else:
                        st.write(response)


