import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# FastAPI endpoints
CLASSIFY_URL = "http://34.83.236.85:8000/classify_image/"
REMOVE_OBJECT_URL = "http://34.83.236.85:8000/remove_object/"

st.title("Image Classification and Object Removal")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

    # Classify image
    if st.button("Classify Image"):
        files = {'file': uploaded_file.getvalue()}
        response = requests.post(CLASSIFY_URL, files=files)
        if response.status_code == 200:
            data = response.json()
            st.write(f"Cluster Name: {data['cluster_name']}")
            st.write(f"Risk Level: {data['risk_level']}")
        else:
            st.write("Error in classification")

    # Remove object
    if st.button("Remove Object"):
        x1 = st.number_input("x1", min_value=0)
        y1 = st.number_input("y1", min_value=0)
        x2 = st.number_input("x2", min_value=0)
        y2 = st.number_input("y2", min_value=0)
        if x2 > x1 and y2 > y1:
            files = {'file': uploaded_file.getvalue()}
            data = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
            response = requests.post(REMOVE_OBJECT_URL, files=files, data=data)
            if response.status_code == 200:
                result_image = Image.open(BytesIO(response.content))
                st.image(result_image, caption="Processed Image.", use_column_width=True)
            else:
                st.write("Error in object removal")
        else:
            st.write("Invalid coordinates")
