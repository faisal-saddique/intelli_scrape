import streamlit as st
from Home import get_final_outline

if "all_content" in st.session_state:

    with st.expander(f"See results"):
        # Display the combined scraped content and desired outline
        st.subheader("Combined Scraped Content:")
        st.write(st.session_state.all_content)

    st.session_state.edited_all_content = st.text_area("Edit the scraped content:",height=700,value=st.session_state.all_content)

    if st.button("Save & Create Outline"):
        st.subheader("Desired Outline:")
        desired_outline = get_final_outline(st.session_state.urls[0], st.session_state.edited_all_content)
        st.write(desired_outline)

else:
    st.warning("Please head over to Home.")