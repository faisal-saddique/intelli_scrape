import streamlit as st
import utils.default_prompt as dp

st.header("Change default prompt")

buffer = st.text_area("**Please enter the new prompt here (Just the first sentence). The one you see right now is the first sentence of the default prompt.**",value=dp.default_prompt,height=4,placeholder=dp.default_prompt)

if st.button("Submit"):
    st.session_state.updated_prompt = buffer

st.write("---")

st.write("**Complete prompt is sent to ChatGPT like this:**")
st.write("""*Please make a short description (about 60 words) and also bullet-point highlights (one short sentence on feature) for this site without any content from previous text generated. Here's the scraped content from this site:*

*SITE:*
*{url}*

*SCRAPED CONTENT:*
*{scraped_content}*

*ANSWER (SHORT DESCRIPTION OF 60 WORDS + A BULLET-POINT HIGHLIGHTS LIST IN MARKDOWN FORMAT):*""")
