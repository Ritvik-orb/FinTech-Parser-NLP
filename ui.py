import streamlit as st
import requests
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="FinTech Document Parser",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Design Theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;900&family=Inter:wght@300;400;500;600;700&display=swap');

* {
    margin: 0;
    padding: 0;
}

html, body {
    background: linear-gradient(135deg, #0d0221 0%, #1a0033 100%);
    min-height: 100vh;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.appViewContainer {
    background: linear-gradient(135deg, #0d0221 0%, #1a0033 100%);
}
}

.main {
    background: linear-gradient(135deg, #0d0221 0%, #1a0033 100%);
    padding: 0 !important;
}

.block-container {
    padding: 3rem 2rem !important;
    max-width: 1200px !important;
    margin: 0 auto;
}

/* Typography */
h1 {
    color: #ffffff;
    text-align: center;
    font-weight: 900;
    margin-bottom: 0.5rem;
    text-shadow: 0 2px 20px rgba(157, 78, 221, 0.2);
    letter-spacing: -1px;
    font-size: 3.5rem !important;
    font-family: 'Playfair Display', serif !important;
    animation: slideDown 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

h2 {
    color: #ffffff;
    font-weight: 700;
    margin: 2rem 0 1rem !important;
    font-size: 2rem;
    font-family: 'Playfair Display', serif !important;
    letter-spacing: -0.5px;
}

h3 {
    color: #c77dff;
    font-weight: 600;
    font-size: 1.3rem;
    margin-bottom: 1.5rem !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.5px;
}

p {
    color: rgba(255, 255, 255, 0.85);
    line-height: 1.8;
    font-weight: 300;
    letter-spacing: 0.3px;
}

/* Animations */
@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #5a189a 0%, #7b2cbf 100%) !important;
    color: white !important;
    border: 2px solid #c77dff !important;
    border-radius: 30px;
    height: 55px;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow: 0 8px 25px rgba(90, 24, 154, 0.3) !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    width: 100%;
    animation: fadeInUp 0.6s ease 0.3s both;
}

.stButton>button:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 35px rgba(157, 78, 221, 0.5) !important;
    background: linear-gradient(135deg, #7b2cbf 0%, #5a189a 100%) !important;
}

.stButton>button:active {
    transform: translateY(-1px);
}

/* File Uploader */
.stFileUploader {
    background: rgba(90, 24, 154, 0.08) !important;
    border-radius: 20px !important;
    padding: 3rem 2rem !important;
    box-shadow: 0 15px 40px rgba(90, 24, 154, 0.12) !important;
    margin: 2.5rem 0 !important;
    animation: fadeInUp 0.6s ease 0.1s both;
    border: 2px solid rgba(199, 125, 255, 0.2) !important;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.stFileUploader:hover {
    box-shadow: 0 20px 50px rgba(157, 78, 221, 0.2) !important;
    transform: translateY(-2px);
    border-color: #c77dff !important;
}

.stFileUploader label {
    color: #c77dff !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    letter-spacing: 0.3px;
    font-family: 'Inter', sans-serif !important;
}

.stFileUploader section label {
    color: #c77dff !important;
    font-weight: 600 !important;
}

/* Messages */
.stSuccess {
    background: linear-gradient(135deg, #5a189a 0%, #7b2cbf 100%) !important;
    border-radius: 15px !important;
    padding: 1.5rem !important;
    color: white !important;
    font-weight: 700 !important;
    box-shadow: 0 8px 20px rgba(157, 78, 221, 0.3);
    animation: fadeInUp 0.5s ease;
    border: 1px solid #c77dff !important;
}

.stError {
    background: linear-gradient(135deg, #7b2cbf 0%, #5a189a 100%) !important;
    border-radius: 15px !important;
    padding: 1.5rem !important;
    color: white !important;
    font-weight: 600 !important;
}

.stInfo {
    background: rgba(90, 24, 154, 0.1) !important;
    border-left: 5px solid #c77dff !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    color: rgba(255, 255, 255, 0.9) !important;
    box-shadow: 0 5px 15px rgba(157, 78, 221, 0.15);
    border: 2px solid rgba(199, 125, 255, 0.15) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 2rem;
    border-bottom: 2px solid rgba(199, 125, 255, 0.2);
}

.stTabs [data-baseweb="tab"] {
    color: rgba(255, 255, 255, 0.7) !important;
    font-weight: 600;
    font-size: 15px;
    padding: 0.8rem 0 !important;
    font-family: 'Inter', sans-serif !important;
}

.stTabs [aria-selected="true"] {
    color: #c77dff !important;
    border-bottom: 3px solid #c77dff;
}

/* Metric/Data Display */
.metric-box {
    background: rgba(90, 24, 154, 0.08);
    border-radius: 16px;
    padding: 1.8rem;
    text-align: center;
    margin: 1rem 0;
    box-shadow: 0 8px 25px rgba(157, 78, 221, 0.1);
    border: 2px solid rgba(199, 125, 255, 0.15);
    transition: all 0.3s ease;
    animation: fadeInUp 0.6s ease;
}

.metric-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 35px rgba(157, 78, 221, 0.2);
    border-color: #c77dff;
}

.metric-box strong {
    display: block;
    color: #c77dff;
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-family: 'Inter', sans-serif;
}

.metric-box span {
    display: block;
    color: rgba(255, 255, 255, 0.95);
    font-size: 1.4rem;
    font-weight: 700;
    word-break: break-word;
    font-family: 'Playfair Display', serif;
}

.entity-value {
    color: #c77dff;
    font-weight: 700;
}

/* Text Area */
.stTextArea textarea {
    border-radius: 12px !important;
    border: 2px solid rgba(199, 125, 255, 0.2) !important;
    background: rgba(26, 0, 51, 0.5) !important;
    color: rgba(255, 255, 255, 0.9) !important;
    font-family: 'Courier New', monospace;
    font-size: 13px;
}

.stTextArea textarea:focus {
    border-color: #c77dff !important;
    box-shadow: 0 0 10px rgba(199, 125, 255, 0.3) !important;
}

/* JSON Display */
.stJson {
    background: linear-gradient(135deg, rgba(90, 24, 154, 0.08) 0%, rgba(26, 0, 51, 0.3) 100%) !important;
    border-radius: 15px !important;
    padding: 2rem !important;
    border: 2px solid rgba(199, 125, 255, 0.15) !important;
    box-shadow: 0 5px 20px rgba(157, 78, 221, 0.1);
}

/* Spinner */
.stSpinner > div {
    border-color: rgba(199, 125, 255, 0.2);
}

.stSpinner > div > div {
    border-color: #c77dff;
    border-top-color: rgba(199, 125, 255, 0.2);
}

/* Divider */
hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(199, 125, 255, 0.2), transparent);
    margin: 3rem 0;
}

/* Footer */
footer {
    text-align: center;
    color: rgba(255, 255, 255, 0.8);
    font-size: 0.95rem;
    margin-top: 3rem;
    padding: 2rem 0;
    border-top: 1px solid rgba(199, 125, 255, 0.15);
}

/* Columns */
.stColumns {
    gap: 2rem;
}

/* Responsive */
@media (max-width: 768px) {
    h1 {
        font-size: 2rem !important;
    }
    
    h2 {
        font-size: 1.4rem;
    }
    
    .block-container {
        padding: 2rem 1rem !important;
    }
    
    .stButton>button {
        height: 48px;
        font-size: 14px;
    }
    
    .metric-box {
        padding: 1.2rem;
    }
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### About This App")
    st.markdown(
        """
        **FinTech Document Parser**
        
        Powered by advanced AI technologies to extract and analyze financial data from documents.
        """
    )
    st.info(
        "Lightning-fast OCR + NLP entity recognition"
    )
    st.markdown("---")
    st.markdown("### Key Features")
    st.markdown("""
    - PDF & Image Support - Handle any format
    - Smart Recognition - AI-powered entity extraction
    - Auto Classification - Identify document type
    - Account Detection - Extract account numbers
    - Download Results - Export as JSON
    """)
    st.markdown("---")
    st.markdown("### Supported Formats")
    st.markdown("""
    - **Documents:** PDF
    - **Images:** PNG, JPG, JPEG
    """)
    st.markdown("---")
    st.markdown("### Tips")
    st.markdown("""
    - Upload clear, high-quality documents
    - Ensure text is readable
    - Larger files may take longer
    """)

# Main Header
st.markdown("<h1>FinTech Document Parser</h1>", unsafe_allow_html=True)
st.markdown("<h3>Extract Financial Data with Advanced AI</h3>", unsafe_allow_html=True)

# Instruction text
st.markdown("""
<div style='text-align: center; margin: 2rem 0;'>
    <p style='color: rgba(255, 255, 255, 0.9); font-size: 1.1rem; font-weight: 500;'>
        Upload your financial document below
    </p>
    <p style='color: rgba(255, 255, 255, 0.7); font-size: 0.95rem;'>
        Supports PDF files and images (PNG, JPG)
    </p>
</div>
""", unsafe_allow_html=True)

# File Upload Section with better layout
col_left, col_upload, col_right = st.columns([0.5, 1.5, 0.5])
with col_upload:
    file = st.file_uploader(
        "Select File",
        type=["pdf", "png", "jpg", "jpeg"],
        label_visibility="collapsed",
        help="Drag and drop a PDF or image file here"
    )

if file:
    try:
        with st.spinner("Analyzing document with AI..."):
            res = requests.post(
                "http://127.0.0.1:8000/upload/",
                files={"file": file},
                timeout=30
            )
            res.raise_for_status()
            data = res.json()

        # Success Message with animation
        st.success("Extraction Complete! Document processed successfully.")

        # Display filename and processing info
        col_info1, col_info2, col_info3 = st.columns(3)
        with col_info1:
            st.markdown(f"<div class='metric-box'><strong>File Name</strong><br><span class='entity-value'>{file.name}</span></div>", unsafe_allow_html=True)
        with col_info2:
            st.markdown(f"<div class='metric-box'><strong>File Size</strong><br><span class='entity-value'>{file.size / 1024:.1f} KB</span></div>", unsafe_allow_html=True)
        with col_info3:
            st.markdown(f"<div class='metric-box'><strong>Processed At</strong><br><span class='entity-value'>{datetime.now().strftime('%H:%M:%S')}</span></div>", unsafe_allow_html=True)

        st.markdown("---")

        # Create result tabs with better styling
        tab1, tab2, tab3 = st.tabs(["Extracted Entities", "Document Text", "Classification"])

        with tab1:
            st.markdown("### Extracted Financial Data")
            entities = data.get("entities", {})
            if entities and any(entities.values()):
                # Create a grid layout for entities
                cols = st.columns(2)
                entity_count = 0
                for key, value in entities.items():
                    if value:
                        with cols[entity_count % 2]:
                            if isinstance(value, list):
                                value_display = ", ".join(str(v) for v in value)
                            else:
                                value_display = str(value)
                            st.markdown(
                                f"""
                                <div class='metric-box'>
                                    <strong>{key}</strong>
                                    <br>
                                    <span class='entity-value'>{value_display}</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        entity_count += 1
                if entity_count == 0:
                    st.info("No specific entities detected in this document")
            else:
                st.info("No entities found. This might be a new or unstructured document type.")

        with tab2:
            st.markdown("### Full Document Text")
            text = data.get("text", "No text extracted")
            # Create expandable text area
            st.text_area(
                "Extracted Content",
                text,
                height=400,
                disabled=True,
                label_visibility="collapsed"
            )
            # Add copy button functionality
            col1, col2 = st.columns([4, 1])
            with col2:
                st.markdown(
                    f"<p style='text-align: center; color: rgba(255, 255, 255, 0.7);'>{len(text)} chars</p>",
                    unsafe_allow_html=True
                )

        with tab3:
            st.markdown("### Document Type")
            doc_type = data.get("type", "Unknown")
            
            # Map document types to descriptions
            type_descriptions = {
                "Bank Statement": "A financial statement from a banking institution",
                "Invoice": "A bill or invoice for products/services",
                "Unknown": "Unrecognized document type"
            }
            
            description = type_descriptions.get(doc_type, "Document type detected")
            
            st.markdown(
                f"""
                <div class='metric-box' style='padding: 3rem; border-radius: 20px;'>
                    <h2 style='color: #667eea; margin: 0;'>{doc_type}</h2>
                    <p style='color: #666; margin-top: 0.5rem;'>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Export Section
        st.markdown("---")
        st.markdown("### Export Results")
        
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            json_str = json.dumps(data, indent=2)
            st.download_button(
                label="Download as JSON",
                data=json_str,
                file_name=f"extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col_export2:
            # Create a text summary for download
            text_summary = f"""FINTECH DOCUMENT EXTRACTION REPORT
=====================================

Document Type: {data.get('type', 'Unknown')}
Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
File Name: {file.name}

EXTRACTED ENTITIES
==================
"""
            entities = data.get("entities", {})
            for key, value in entities.items():
                if value:
                    text_summary += f"\n{key}: {value}\n"
            
            text_summary += f"\n\nFULL TEXT\n=========\n{data.get('text', 'No text extracted')}"
            
            st.download_button(
                label="Download as Text",
                data=text_summary,
                file_name=f"extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

        # Summary statistics
        st.markdown("---")
        st.markdown("### Processing Summary")
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            entities = data.get("entities", {})
            entity_count = sum(1 for v in entities.values() if v)
            st.metric("Entities Found", entity_count)
        
        with col_stat2:
            text = data.get("text", "")
            st.metric("Text Length", f"{len(text)}")
        
        with col_stat3:
            text = data.get("text", "")
            words = len(text.split())
            st.metric("Words", words)
        
        with col_stat4:
            st.metric("Status", "Success")

    except requests.exceptions.ConnectionError:
        st.error("Connection Error\nCannot connect to the API server. Please ensure FastAPI is running on http://127.0.0.1:8000")
    except requests.exceptions.Timeout:
        st.error("Timeout Error\nThe server took too long to respond. Please try again with a smaller file.")
    except Exception as e:
        st.error(f"Error Processing Document\n\n{str(e)}")
        st.info("Try uploading a different document or contact support if the issue persists.")

# Footer
st.markdown("---")
st.markdown(
    """
    <footer>
        <p style='margin: 0;'>Built with heart for Financial Data Extraction</p>
        <p style='margin: 0.5rem 0 0 0; opacity: 0.8;'>Powered by Advanced NLP & OCR & FastAPI</p>
    </footer>
    """,
    unsafe_allow_html=True
)
