import streamlit as st
import streamlit.components.v1 as v1

st.set_page_config(page_title="Test Site", layout="wide")


col1, col2 = st.columns(2)

with col1:
    userInput = st.text_area("Input:")
    #test

with col2:
    generatedText = st.text_area("Output:", key="Output")
    #test


#Testbox
html_string='''
    <textarea name="" id="" cols="30" rows="4" class="textarea-test"></textarea>
    <script>
        console.log(document);
        const textArea = document.querySelector(".textarea-test")

        textArea.addEventListener('input', (e) => {
            textArea.style.height = "auto"
            textArea.style.height = `${textArea.scrollHeight}px`;
            console.log("pass");
        })
    </script>
'''

v1.html(html_string)

def disable(b):
    st.session_state["disabled"] = b

button_a = st.button('a', key='but_a', on_click=disable, args=(False,))
button_b = st.button('b', key='but_b', on_click=disable, args=(True,))
button_c = st.button('c', key='but_c', disabled=st.session_state.get("disabled", True))

from PIL import Image

image = Image.open('Eviden_orange.png')

st.image(image, caption='Sunrise by the mountains')
