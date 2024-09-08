import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body_contents, extract_body
from parse import parse_with_ollama, pasrse_with_openai


st.title("AI Web Scraper")
url = st.text_input("Enter Web Site URL:")

if st.button("Scrape Site"):
    st.write("Scraping...")
    result = scrape_website(url)
    body_content = extract_body(result)
    cleaned_contain = clean_body_contents(body_content)
    
    st.session_state.dom_content = cleaned_contain
    
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_contain, height=300)
        
if "dom_content" in st.session_state:
    pasre_description = st.text_area("Descrive what you want to parse?")
    
    input_type = st.radio(
        "Select Model",
        ("OPENAI", "OLLAMA")
    )
    
    if st.button("Parse Content"):
        st.write("Parsing the content")
        result = ""
        
        dom_chunks = split_dom_content(st.session_state.dom_content)
        if input_type == "OPENAI":
            result = pasrse_with_openai(dom_chunks, pasre_description)
        elif input_type == "OLLAMA":
            result = parse_with_ollama(dom_chunks, pasre_description)
        st.write(result)