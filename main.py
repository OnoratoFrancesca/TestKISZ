import textstat
import streamlit as st
from utils import ask_openai
from PIL import Image
# ---- helper functions ----

# IMPLEMENT LATER

def getFleschGer(inputStr):
    return textstat.textstat.flesch_reading_ease(inputStr)

def getFleschKin(inputStr):
    return 0

def getGobbledygook(inputStr):
    return 0

def getWiener(inputStr):
    return textstat.textstat.wiener_sachtextformel(inputStr,2)

def getLix(inputStr):
    return textstat.textstat.lix(inputStr)

def getHohenheimer(inputStr):
    return 0

def generateAItext(query, prompt):
    return ask_openai(query=query,prompt=prompt)


# ---- initialize ----

st.set_page_config(page_title="Einfache Sprache", layout="wide")
inputstr = ""
aistr = ""
prompt = ""
query = ""



# ---- Header Section ----
with st.container():
    st.title("Einfache Sprache")
    col1, col2 = st.columns(2)
    with col1:
        prompt = st.text_area("Prompt:")
        st.session_state["promptState"] = prompt

    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        center_button = st.button('Einfachen Text generieren')
        if center_button:
            st.session_state["response"] = generateAItext(st.session_state["queryState"], st.session_state["promptState"])
            #st.experimental_rerun()
            st.generatedText = st.session_state["response"]




# ---- Check einfache Sprache ----
with st.container():
    st.write('---')
    left_column, right_column = st.columns(2)
    st.write('---')
    left_res_column, right_res_column = st.columns(2)

# ---- text check ----
    with left_column:
        st.subheader("Bitte geben Sie hier den zu prüfenden Text ein:")
        query = st.text_area("Eigener Text:", height=300)
        st.session_state["queryState"] = query
        if st.button("Check"):
            with left_res_column:
                aistr = st.session_state["response"]
                st.subheader("Ergebnis der Prüfung des eigenen Textes:")
                d = {"Readability index":
                         ["Flesch-Reading-Ease German",
                         # "Flesch-Kincaid-Grade-Level",
                          #"Simple Measure of Gobbledygook",
                          "Wiener Sachtextformel",
                          "Lesbarkeitsindex (LIX)"],
                          #"Hohenheimer Index"],
                     "Result":
                         [getFleschGer(query),
                         # getFleschKin(query),
                         # getGobbledygook(query),
                          getWiener(query),
                          getLix(query)],
                         # getHohenheimer(query)],
                     "Bad-Good":
                         ["0-100",
                         # "12-0",
                         # "18-5",
                          "15-4",
                          "60-20"]}
                        #  "N/A"
                         
                st.table(d)

                with right_res_column:
                    st.subheader("Ergebnis der Prüfung des generierten Textes:")
                    d2 = {"Readability index":
                              ["Flesch-Reading-Ease German",
                             #  "Flesch-Kincaid-Grade-Level",
                             #  "Simple Measure of Gobbledygook",
                               "Wiener Sachtextformel",
                               "Lesbarkeitsindex (LIX)"],
                              # "Hohenheimer Index"],
                          "Result":
                              [getFleschGer(aistr),
                          #     getFleschKin(aistr),
                           #    getGobbledygook(aistr),
                               getWiener(aistr),
                               getLix(aistr)],
                            #   getHohenheimer(aistr)],
                          "Bad-Good":
                              ["0-100",
                              # "12-0",
                               #"18-5",
                               "15-4",
                               "60-20"
                               #"N/A"
                               ]}
                    st.table(d2)





# ---- AI generated text ----

    if "response" not in st.session_state:
        st.session_state["response"] = ""
    if "queryState" not in st.session_state:
        st.session_state["queryState"] = ""
    if "promptState" not in st.session_state:
        st.session_state["promptState"] = ""

    with right_column:
        st.subheader("Generierter \"leichter\" Text")
        aistr = st.text_area("AI:", height=300,key ="generatedText", value=st.session_state["response"])

# --- results container with plot
with st.expander("Visualise results"):
    image = Image.open('results_table.png')
    st.image(image, caption='Metrics calculated on generated texts')

