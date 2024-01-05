import streamlit as st


def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://i.imgur.com/At86a7L.png);
                background-repeat: no-repeat;
                background-size:45%;
                background-position: 20px 20px;
            }
            .css-ng1t4o {{width: 10rem;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def app() -> None:
    # config
    st.set_page_config(
        page_title="LegalLens AI",
        page_icon="🔍",
        layout="wide",
        menu_items={"Get help": None, "Report a bug": None},
    )
    add_logo()

    st.title("🔍 LegalLens AI")

    st.header("Information")
    st.markdown(
        """
        The AI counsel companion for lawyers to support their client communications
        ....
        ....
        ....
        """
    )

    st.subheader("Hello from XXXX 👋")
    st.markdown(
        """
        Some fancy bull for landing page, team intro, value proposition, reaching out, call for help
        """
    )


if __name__ == "__main__":
    # run as a script to test streamlit app locally
    app()
