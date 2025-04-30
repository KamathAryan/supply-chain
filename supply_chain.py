import streamlit as st
import pandas as pd
from PIL import Image
from PIL import ImageOps
import os
import streamlit.components.v1 as components
import base64
import openpyxl
# Set page config at the very top
st.set_page_config(layout="wide")

# Remove top padding and add custom styles
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
        }
        .info-box {
            background-color: #f0f9ff;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #d3e5ef;
            margin-top: 10px;
        }
        .info-label {
            font-weight: bold;
            color: #005577;
            display: inline-block;
            width: 150px; /* You can adjust the width for better spacing */
        }
        .info-value {
            display: inline-block;
            color: #333;
            margin-left: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Load the Excel data
try:
    df = pd.read_excel("data.xlsx", engine='openpyxl')
    df = df[df["part_no"].notna()]
except Exception as e:
    st.error(f"Error loading Excel file: {e}")
    df = pd.DataFrame()

# Header
st.markdown("<h1 style='color:#009999; margin-bottom: 0;'>Siemens Supply Chain</h1>", unsafe_allow_html=True)
st.markdown("<hr style='margin-top: 0;'>", unsafe_allow_html=True)

if not df.empty:
    part_list = df["part_no"].tolist()
    selected_part = st.selectbox("Select a Part No.", part_list)

    selected_row = df[df["part_no"] == selected_part].iloc[0]

    # Wider left column for info
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown("### Part Information")
        fields_to_show = {
            "Description": "object_description",
            "Supplier": "supplier",
            "V Code": "v_code",
            "Category": "Category"
        }

        for label, field in fields_to_show.items():
            st.markdown(f"""
                <div class="info-box">
                    <div class="info-label">{label}</div>
                    <div class="info-value">{selected_row[field]}</div>
                </div>
            """, unsafe_allow_html=True)
        datasheet_name = selected_row["datasheet"]
        datasheet_path = os.path.join("static", "datasheet_folder", datasheet_name)
        if os.path.exists(datasheet_path):
            datasheet_download_button = f"""
            <div class="info-box">
                <div class="info-label">Datasheet</div>
                <div class="info-value">
                    <a href="data:application/pdf;base64,{base64.b64encode(open(datasheet_path, 'rb').read()).decode()}"
                    download="{datasheet_name}" style="text-decoration: none; color: #007acc;">
                    Download {datasheet_name}
                    </a>
                </div>
            </div>
            """
            st.markdown(datasheet_download_button, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="info-box">
                    <div class="info-label">Datasheet</div>
                    <div class="info-value">No datasheet available.</div>
                </div>
            """, unsafe_allow_html=True)

                

    with col2:

        image_path = os.path.join("image_folder", selected_row["image_name"])
        placeholder_path = os.path.join("image_folder", "image_not_found.jpg")
        image_display_path = image_path if os.path.exists(image_path) else placeholder_path

        try:
            with Image.open(image_display_path) as img:
                img = ImageOps.exif_transpose(img)
                img = img.convert("RGB")
                aspect_ratio = img.height / img.width
                new_width = 400
                new_height = int(new_width * aspect_ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                st.image(img, caption="Part Image", use_container_width=False)
        except Exception as e:
            st.warning(f"Could not load even the placeholder image: {e}")
        # datasheet_name = selected_row["datasheet"]
        # datasheet_path = os.path.join("static", "datasheet_folder", datasheet_name)
        # datasheet_name = selected_row["datasheet"]
        # datasheet_path = os.path.join("static", "datasheet_folder", datasheet_name)

        # if os.path.exists(datasheet_path):
        #     with open(datasheet_path, "rb") as f:
        #         st.download_button(
        #             label="📄 Download Datasheet",
        #             data=f,
        #             file_name=datasheet_name,
        #             mime="application/pdf"
        #         )
        # else:
        #     st.info("No datasheet available.")


else:
    st.warning("No valid data found in Excel file.")
