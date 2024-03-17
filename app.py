import duckdb
import pandas as pd
import streamlit as st
from streamlit.errors import StreamlitAPIException

st.write("Hello world")
data = {"a": [1,2,3], "b": [4,5,6]}
df = pd.DataFrame(data)

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])
try:
    with tab1:
        input_text = st.text_area(label = "entrez votre input")
        st.write(input_text)
        st.dataframe(duckdb.sql(input_text).fetchdf())

except StreamlitAPIException as s:
    # Continue with the code
    st.dataframe(duckdb.sql(input_text))

with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)