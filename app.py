import streamlit as st
import requests
from docx import Document
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")

st.write(
    "Generate professional legal document templates using "
    "Google Gemini AI."
)


st.header("Document Information")


document_type = st.selectbox(
    "Document Type",
    [
        "Freelance Work Contract",
        "Non-Disclosure Agreement",
        "Employment Agreement",
        "Rental Agreement",
        "Service Agreement",
        "Partnership Agreement",
        "Other"
    ]
)


parties = st.text_area(
    "Parties",
    placeholder="Example: Jane Doe (Service Provider), TechNova Inc. (Client)"
)


terms = st.text_area(
    "Terms & Conditions",
    placeholder="Enter the important terms and conditions..."
)


dates = st.date_input("Effective Date")


if st.button("Generate Document", type="primary"):

    if not parties.strip():
        st.error("Please enter the parties involved.")
        st.stop()

    if not terms.strip():
        st.error("Please enter the terms and conditions.")
        st.stop()

    request_data = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "dates": dates.strftime("%B %d, %Y")
    }

    try:

        with st.spinner("Generating your legal document..."):

            response = requests.post(
                "http://127.0.0.1:8000/generate",
                json=request_data,
                timeout=120
            )

        if response.status_code == 200:

            result = response.json()

            st.session_state["document"] = result["content"]
            st.session_state["document_type"] = document_type

            st.success("Document generated successfully!")

        else:

            st.error(
                f"Document generation failed: {response.text}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "Could not connect to the FastAPI server. "
            "Please make sure Uvicorn is running."
        )

    except requests.exceptions.Timeout:

        st.error(
            "The server took too long to respond. "
            "Please try generating the document again."
        )

    except Exception as e:

        st.error(f"Error: {str(e)}")


if "document" in st.session_state:

    st.divider()

    st.header("Generated Document")

    edited_document = st.text_area(
        "Edit your document if needed:",
        value=st.session_state["document"],
        height=600
    )

    st.session_state["document"] = edited_document

    st.divider()

    st.subheader("Download Document")


    # TXT DOWNLOAD

    st.download_button(
        "📄 Download TXT",
        data=st.session_state["document"],
        file_name="legalease_document.txt",
        mime="text/plain",
        key="download_txt"
    )


    # DOCX DOWNLOAD

    doc = Document()

    for paragraph in st.session_state["document"].split("\n"):
        doc.add_paragraph(paragraph)

    docx_file = BytesIO()

    doc.save(docx_file)

    docx_file.seek(0)

    st.download_button(
        "📝 Download DOCX",
        data=docx_file,
        file_name="legalease_document.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        key="download_docx"
    )


    # PDF DOWNLOAD

    pdf_file = BytesIO()

    styles = getSampleStyleSheet()

    pdf = SimpleDocTemplate(
        pdf_file,
        pagesize=A4
    )

    story = []

    for line in st.session_state["document"].split("\n"):

        if line.strip():

            safe_line = (
                line
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )

            story.append(
                Paragraph(
                    safe_line,
                    styles["Normal"]
                )
            )

    pdf.build(story)

    pdf_file.seek(0)

    st.download_button(
        "📕 Download PDF",
        data=pdf_file,
        file_name="legalease_document.pdf",
        mime="application/pdf",
        key="download_pdf"
    )
