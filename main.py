import datetime
from PIL import Image
import streamlit as st
import utils
import os
import openai
from csv import writer
import blobupload
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# ---- helper functions ----
def generateAItext(query, prompt):
    #with OpenAI
    #return utils.ask_openai(query=query, prompt=prompt)
    
    #with Azure OpenAI
    return utils.ask_azure("""Bitte extrahieren Sie die wichtigsten Informationen aus dem komplexen Artikel zwischen ``. Wandeln sie diesen Text in einfache Sprache um. 
Achten sie darauf, dass sie die extrahierten Informationen im Text berücksichtigen. 
Falls der komplexen Artikel zwischen `` weniger als 6 Wörter beinhaltet, schreiben Sie "Schreiben Sie bitte einen längeren Text!".
Falls der komplexen Artikel zwischen `` mehr als 6 Wörter beinhaltet fahren Sie fort.

Regeln für die Einfache Sprache:

Verwenden Sie kurze Sätze (maximal 5 bis 8 Wörter), um Ideen klar auszudrücken.

Begrenzen Sie jeden Absatz auf eine einzige Aussage oder Information.

Verwenden Sie nur Aktiv anstatt Passiv, ohne den Inhalt zu verfremden.

Vermeiden Sie Fachbegriffe oder verwenden Sie einfache Erklärungen dafür. 

Benutzen Sie einen einfachen Wortschatz.

Stellen Sie sicher, dass jeder Abschnitt auf die Hauptpunkte des Artikels verweist.

Kürzen Sie Nebeninformationen und konzentrieren Sie sich auf das Wesentliche.

Überprüfen Sie regelmäßig, ob der Text verständlich und klar bleibt.

Vermeiden Sie Nebensätze, wenn möglich.

Hinweis: Das Ziel ist es, den Artikel so einfach und verständlich wie möglich darzustellen, ohne dabei wesentliche Informationen zu verlieren.
``{}``

Nachdem Sie den Artikel in einfacher Sprache wiedergegeben haben, überprüfen Sie bitte, ob der Text leicht verständlich ist und die Hauptpunkte des ursprünglichen Artikels vermittelt werden.
Geben Sie nur die Übersetzung in einfacher Sprache zurück.""".format(query))

def check():
    with left_res_column:
        aistr = st.session_state["response"]
        query = st.session_state["queryState"]
        st.subheader("Ergebnis der Prüfung des eigenen Textes:")
        st.write("Niveau: " + utils.calulateDifficultyNiveau(query))
        st.pyplot(utils.create_horizontal_bar_chart(utils.calculateDifficultyPercentage(query)))
        with st.expander(label="Mehr Infos"):
            d = {"Readability index":
                     ["Flesch-Reading-Ease German",
                      "Wiener Sachtextformel",
                      "Lesbarkeitsindex (LIX)"],
                 "Result":
                     [utils.getFleschGer(query),
                      utils.getWiener(query),
                      utils.getLix(query)],
                 "Bad-Good":
                     ["0-100",
                      "15-4",
                      "60-20"]}

            st.table(d)

        with right_res_column:
            st.subheader("Ergebnis der Prüfung des generierten Textes:")
            st.write("Niveau: " + utils.calulateDifficultyNiveau(aistr))
            st.pyplot(utils.create_horizontal_bar_chart(utils.calculateDifficultyPercentage(aistr)))
            with st.expander(label="Mehr Infos"):
                d2 = {"Readability index":
                          ["Flesch-Reading-Ease German",
                           "Wiener Sachtextformel",
                           "Lesbarkeitsindex (LIX)"],
                      "Result":
                          [utils.getFleschGer(aistr),
                           utils.getWiener(aistr),
                           utils.getLix(aistr)],
                      "Bad-Good":
                          ["0-100",
                           "15-4",
                           "60-20"]}
                st.table(d2)


st.set_page_config(page_title="Magic Simplifier", layout="wide")


# ---- Authentication ----
config = ""
with open('creds.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)
name, authentication_status, username = authenticator.login('Login', 'main')
if st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
elif st.session_state["authentication_status"]:

    #Header Section
    with st.container():
        leftheader,middleheader, rightheader = st.columns(3)
        with rightheader:
            st.write(" ")
            st.write(" ")
            shcol1, shcol2, shcol3 = st.columns(3)
            with shcol1:
                st.markdown("<p style='text-align: right; black: red;'>Powered by:</p>", unsafe_allow_html=True)
            with shcol2:
                evidenlogo = Image.open("Eviden_orange.png")
                st.image(evidenlogo)
            with shcol3:
                swmhlogo = Image.open("Südwestdeutsche_Medienholding_Logo.png")
                st.image(swmhlogo)
        with leftheader:
            st.title("Magic Simplifier")
        st.write("---")


    # ---- initialize ----

    inputstr = ""
    aistr = ""
    prompt = ""
    query = ""
    #save here value api key if you don't want to input it at every app run
    os.environ['OPENAI_API_KEY']="50520055ef274def8b4e65960f284b8f"
    openai.api_key="50520055ef274def8b4e65960f284b8f"



    # ---- Check einfache Sprache ----
    with st.container():
        col1,col2,col3,col4,col5=st.columns(5)

        left_column, right_column = st.columns(2)
        st.write('---')
        left_res_column, right_res_column = st.columns(2)
        st.write("---")


        # ---- text check ----
        with col1:
            st.write(f'Welcome *{st.session_state["name"]}*!')
        with col5:
            colincol1, colincol2, colincol3 = st.columns(3)
            with colincol3:
                authenticator.logout('Logout', 'main')
        with col3:
            center_button = st.button('Leichten Text generieren')
            if center_button:
                st.session_state["response"] = generateAItext(st.session_state["queryState"], st.session_state["promptState"])
                st.generatedText = st.session_state["response"]
                check()
                if "uniqueID" not in st.session_state:
                    st.session_state["uniqueID"] = ""
                st.session_state["uniqueID"] = datetime.datetime.now()
                List = [st.session_state["queryState"], st.session_state["response"], st.session_state["name"], st.session_state["uniqueID"]]
                with open('inputAndOutput.csv', "w") as f_object:
                    writer_objet = writer(f_object)
                    writer_objet.writerow(List)
                    f_object.close()
                blobupload.uploadToBlob2()

        with left_column:
            st.subheader("Ausgangstext:")
            query = st.text_area("Eigener Text:", height=300)
            st.session_state["queryState"] = query
            if st.button("Schwierigkeit berechnen"):
                check()

        # ---- AI generated easy-text ----

        if "response" not in st.session_state:
            st.session_state["response"] = ""
        if "queryState" not in st.session_state:
            st.session_state["queryState"] = ""
        if "promptState" not in st.session_state:
            st.session_state["promptState"] = ""

        with right_column:
            st.subheader("Generierte Leichte Sprache:")
            aistr = st.text_area("AI:", height=300, key="generatedText", value=st.session_state["response"])

    #Added Feedback
    with st.container():
        if "qualityFeedback" not in st.session_state:
            st.session_state["qualityFeedback"] = "nichts"
        if "feedback" not in st.session_state:
            st.session_state["feedback"] = "unassigned"
        left_feedback_col, right_feedback_col = st.columns(2)
        with left_feedback_col:
            st.subheader("Disclaimer für das KI-Tool von Eviden Deutschland GmbH:")
            st.markdown("""
            1. Die Eviden Deutschland GmbH bietet ein KI-Tool zur automatischen Textgenerierung an. Die Haftung für Inhalt und juristische Korrektheit der generierten Texte wird ausgeschlossen. 
            1. Die Nutzung des KI-Tools erfolgt auf eigenes Risiko. Die Eviden Deutschland GmbH übernimmt keine Verantwortung für die Richtigkeit, Vollständigkeit oder Aktualität der generierten Texte.
            1. Die generierten Texte stellen keine rechtliche Beratung dar und sollten nicht als solche interpretiert werden. Bei rechtlichen Fragen sollte professioneller Rat eingeholt werden.
            1. Jegliche Schäden oder Konsequenzen, die aus der Verwendung der generierten Texte resultieren, liegen in der Verantwortung des Nutzenden. Dies schließt direkte und indirekte Schäden ein.
            1. Das Urheberrecht der generierten Texte liegt bei der SWMH. Eine Nutzung ohne Genehmigung ist untersagt.  
            Stand: 24.08.2023""")
        with right_feedback_col:
            st.subheader("Feedback")
            st.write("Wie fanden Sie den generierten Text?")
            fcol1,fcol2,fcol3,fcol4,fcol5,fcol6,fcol7,fcol8 = st.columns(8)
            selectedFeedback = "nichts"
            st.write("Sie haben " + st.session_state["qualityFeedback"] + " ausgewählt!")
            with fcol4:
                thumbsdown = st.button(":-1:")
                if thumbsdown:
                    st.session_state["feedback"] = "bad"
                    st.session_state["qualityFeedback"] = ":-1:"
                    st._rerun()
            with fcol5:
                thumbsup = st.button(":+1:")
                if thumbsup:
                    st.session_state["feedback"] = "good"
                    st.session_state["qualityFeedback"] = ":+1:"
                    st._rerun()
            comment = st.text_area("Kommentar:", placeholder="Hier können Sie einen Kommentar zum generierten Text einfügen!")
            sendFeedback = st.button("Feedback senden")
            if sendFeedback:
                List = [st.session_state["uniqueID"], st.session_state["feedback"], comment]
                with open('Feedback.csv', "w") as f_object:
                    writer_objet = writer(f_object)
                    writer_objet.writerow(List)
                    f_object.close()
                blobupload.uploadToBlob()
                st.info("Feedback erfolgreich gesendet!")



    #implement later
    def disableFeedback():
        pass

