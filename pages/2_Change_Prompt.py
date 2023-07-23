import streamlit as st
import utils.default_prompt as dp

st.header("Change default prompt")

if "updated_prompt" in st.session_state:
    buffer = st.text_area("**Please enter the new prompt here (Just the first sentence). The one you see right now is the first sentence of the default prompt.**",value=st.session_state.updated_prompt,height=4,placeholder=st.session_state.updated_prompt)
else:
    buffer = st.text_area("**Please enter the new prompt here (Just the first sentence). The one you see right now is the first sentence of the default prompt.**",value=dp.default_prompt,height=4,placeholder=dp.default_prompt)
if st.button("Submit"):
    st.session_state.updated_prompt = buffer

st.write("---")

st.write("**Complete prompt is sent to ChatGPT like this:**")

if "updated_prompt" in st.session_state:
    st.write(f"""*{st.session_state.updated_prompt}*""")
else:
    st.write(f"""*{dp.default_prompt}*""")



st.write("""
         
*SITE:*
*{url}*

*SCRAPED CONTENT:*
*{scraped_content}*

*REQUIRED FORMAT OF RESPONSE:*
*A description of the specified word length, followed by a bulled points list in the markdown format.*

*RESPONSE:*""")
