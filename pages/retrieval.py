import streamlit as st
import json
from streamlit_modal import Modal
import base64

def add_logo():
    st.markdown(
       """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://i.imgur.com/At86a7L.png);
                background-repeat: no-repeat;
                background-size: 45%;
                background-position: 20px 20px;
            }
             .css-ng1t4o {{width: 10rem;}}
        </style>
        """,
        unsafe_allow_html=True,
    )

def on_more_click(show_more, idx):
    show_more[idx] = True


def on_less_click(show_more, idx):
    show_more[idx] = False

def on_view_file(filename):
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
    modal = Modal(filename, "key")
    with modal.container():
            # html_string = '''
            # <h1>HTML string in RED</h1>

            # <script language="javascript">
            # document.querySelector("h1").style.color = "red";
            # </script>
            # '''
            # components.html(html_string)
            # value = st.checkbox("Check me")
            # st.write(f"Checkbox checked: {value}")
            with open("./data/files/1.pdf","rb") as f:
                  base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            pdf_display = f'<p align="center"><iframe src="data:application/pdf;base64,{base64_pdf}" width="1400" height="550" type="application/pdf"></iframe></p>'
            # pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width={str(ui_width)} height={str(ui_width*4/3)} type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
            st.write("Applied Laws AI")
            st.markdown("""---""")
            st.write("Some AI features and text etc")
    modal.open()


        


def retrieval_form_container() -> None:
    form = st.form(key="retrieval_query")
    rag_query = form.text_area(
        "Case Retrieval Query", value="Please describe the cases you are interested in here."
    )

    if form.form_submit_button("Search"):
        with st.status("Running"):
            with open('data.json') as f:
                response = json.load(f)
        st.session_state["history"].append(dict(query=rag_query, response=response))
    



def history_display_container(history):
    if len(history) > 1:
        st.header("Search History")
        max_idx = len(history) - 1
        history_idx = st.slider("History", 0, max_idx, value=max_idx, label_visibility="collapsed")
        entry = history[history_idx]
    else:
        entry = history[0]

    st.subheader("Query")
    st.write(entry["query"])

    st.subheader("Retrieved Documents")

    if "show_more" not in st.session_state:
        st.session_state["show_more"] = dict.fromkeys(range(0, len(entry["response"])), False)
    show_more = st.session_state["show_more"]

    cols = st.columns((3, 1, 2, 1.5, 1.5, 1.5, 1))
    fields = ["Case Name", "Added On", "client", "Unique Course Identifier", "Judgement Number", "published year", "view"]

    # header
    for col, field in zip(cols, fields):
        col.write("**" + field + "**")

    # rows
    for idx, row in enumerate(entry["response"]):
        col1, col2, col3, col4, col5, col6, col7 = st.columns((3, 1, 2, 1.5, 1.5, 1.5, 1))
        col1.write(str(row["case_name"]))
        col2.write(str(row["added_on"]))
        col3.write(str(row["client"]))
        col4.write(str(row["UCI"]))
        col5.write(str(row["JN"]))
        col6.write(str(row["year"]))
        

        placeholder = col7.empty()

        if show_more[idx]:
            placeholder.button(
                "Close", key=str(idx) + "_", on_click=on_less_click, args=[show_more, idx]
            )

            # do stuff
            st.write("*Case Summary*")
            st.write(row["summary"])
            st.markdown("""---""")
            for id, file in enumerate(row["files"]):
                col1, col2, = st.columns(2)
                col1.markdown(f"{file}")
                col2.button(
                "view", key=str(idx) + "view" + file + str(id), on_click=on_view_file, args=[file]
                ) 
        else:
            placeholder.button(
                "Show Files",
                key=idx,
                on_click=on_more_click,
                args=[show_more, idx],
                type="primary",
            )


def app() -> None:
    """Streamlit entrypoint for PDF Summarize frontend"""
    # config
    st.set_page_config(
        page_title="📤 retrieval",
        page_icon="📚",
        layout="wide",
        menu_items={"Get help": None, "Report a bug": None},
    )
    add_logo()

    st.title("📤 Retrieval")

    st.markdown(
        """
    Your chatAI based search will list the documents you are looking for.
    """
    )
    st.markdown("""---""")

    retrieval_form_container()

    if history := st.session_state.get("history"):
        history_display_container(history)
    else:
        st.session_state["history"] = list()


if __name__ == "__main__":
    # run as a script to test streamlit app locally
    app()
