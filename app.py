import streamlit as st
import ollama
from PIL import Image
import io
import base64
import json

# Page configuration
st.set_page_config(
    page_title="Receipt Analyzer",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description in main area
try:
    st.markdown("""
        # <img src="data:image/png;base64,{}" width="50" style="vertical-align: -12px;"> Receipt & Warranty Analyzer
    """.format(base64.b64encode(open("./assets/gemma3.png", "rb").read()).decode()), unsafe_allow_html=True)
except:
    st.title("Receipt & Warranty Analyzer")

# Add clear button to top right
col1, col2 = st.columns([6,1])
with col2:
    if st.button("Clear 🗑️"):
        if 'receipt_info' in st.session_state:
            del st.session_state['receipt_info']
        st.rerun()

st.markdown('<p style="margin-top: -20px;">Extract product and warranty information from your receipts!</p>', unsafe_allow_html=True)
st.markdown("---")

# Move upload controls to sidebar
with st.sidebar:
    st.header("Upload Receipt")
    uploaded_file = st.file_uploader("Choose receipt image...", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        try:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Receipt")
            
            if st.button("Analyze Receipt 🔍", type="primary"):
                with st.spinner("Analyzing receipt..."):
                    try:
                        # Convert image to base64
                        image_bytes = uploaded_file.getvalue()
                        
                        response = ollama.chat(
                            model='gemma3:12b',
                            messages=[{
                                'role': 'user',
                                'content': """Analyze this receipt/bill image and extract the following information. 
                                You MUST respond with ONLY a valid JSON object and nothing else. No explanations, no markdown, just the JSON.
                                Use these exact fields (use null for missing information):

                                {
                                    "product": {
                                        "name": "",
                                        "model": "",
                                        "price": "",
                                        "quantity": "",
                                        "specifications": "",
                                        "serial_number": ""
                                    },
                                    "purchase": {
                                        "date": "",
                                        "store_name": "",
                                        "store_location": "",
                                        "transaction_id": ""
                                    },
                                    "warranty": {
                                        "duration": "",
                                        "expiry_date": "",
                                        "terms": "",
                                        "extended_warranty": null
                                    },
                                    "contact": {
                                        "store_phone": "",
                                        "customer_service": "",
                                        "website": "",
                                        "email": "",
                                        "service_centers": []
                                    }
                                }

                                Ensure:
                                1. All dates are in ISO format (YYYY-MM-DD)
                                2. Prices are numerical values without currency symbols
                                3. Your response is ONLY the JSON object, nothing else""",
                                'images': [image_bytes]
                            }]
                        )
                        
                        # Parse the response into JSON
                        try:
                            # Display raw response for debugging
                            st.text("Raw response:")
                            st.text(response.message.content)
                            
                            # Try to clean the response by finding the JSON object
                            content = response.message.content
                            # Find the first { and last }
                            start = content.find('{')
                            end = content.rfind('}') + 1
                            if start != -1 and end != -1:
                                json_str = content[start:end]
                                receipt_data = json.loads(json_str)
                                st.session_state['receipt_info'] = receipt_data
                            else:
                                raise json.JSONDecodeError("No JSON object found in response", content, 0)
                        except json.JSONDecodeError as e:
                            st.error(f"Failed to parse the response into JSON format: {str(e)}")
                            st.error("Please try again or contact support if the issue persists.")
                            st.session_state['receipt_info'] = None
                    except Exception as e:
                        st.error(f"Error analyzing receipt: {str(e)}")
                        st.session_state['receipt_info'] = None
        except Exception as e:
            st.error(f"Error loading image: {str(e)}")

# Main content area for results
if 'receipt_info' in st.session_state:
    # Add download buttons
    col1, col2, col3 = st.columns([4,1,1])
    with col2:
        # Download JSON
        if st.button("JSON 📥"):
            st.download_button(
                label="Download JSON",
                data=json.dumps(st.session_state['receipt_info'], indent=2),
                file_name="receipt_analysis.json",
                mime="application/json"
            )
    with col3:
        # Download formatted text
        if st.button("Text 📄"):
            formatted_text = f"""# Receipt Analysis

## Product Information
- Name: {st.session_state['receipt_info']['product']['name']}
- Model: {st.session_state['receipt_info']['product']['model']}
- Price: {st.session_state['receipt_info']['product']['price']}
- Quantity: {st.session_state['receipt_info']['product']['quantity']}
- Specifications: {st.session_state['receipt_info']['product']['specifications']}
- Serial Number: {st.session_state['receipt_info']['product']['serial_number']}

## Purchase Details
- Date: {st.session_state['receipt_info']['purchase']['date']}
- Store: {st.session_state['receipt_info']['purchase']['store_name']}
- Location: {st.session_state['receipt_info']['purchase']['store_location']}
- Transaction ID: {st.session_state['receipt_info']['purchase']['transaction_id']}

## Warranty Information
- Duration: {st.session_state['receipt_info']['warranty']['duration']}
- Expiry Date: {st.session_state['receipt_info']['warranty']['expiry_date']}
- Terms: {st.session_state['receipt_info']['warranty']['terms']}
- Extended Warranty: {st.session_state['receipt_info']['warranty']['extended_warranty']}

## Contact Information
- Store Phone: {st.session_state['receipt_info']['contact']['store_phone']}
- Customer Service: {st.session_state['receipt_info']['contact']['customer_service']}
- Website: {st.session_state['receipt_info']['contact']['website']}
- Email: {st.session_state['receipt_info']['contact']['email']}
- Service Centers: {', '.join(st.session_state['receipt_info']['contact']['service_centers']) if st.session_state['receipt_info']['contact']['service_centers'] else 'None'}
"""
            st.download_button(
                label="Download Text",
                data=formatted_text,
                file_name="receipt_analysis.txt",
                mime="text/plain"
            )
    
    # Display the results
    st.markdown("### Analysis Results")
    st.json(st.session_state['receipt_info'])
else:
    st.info("Upload a receipt and click 'Analyze Receipt' to extract product and warranty information.")

# Footer
st.markdown("---")