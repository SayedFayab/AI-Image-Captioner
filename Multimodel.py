import streamlit as st
from PIL import Image
import io, base64, os
from openai import OpenAI

# --- Page Config ---
st.set_page_config(page_title="AI Image Captioning", page_icon="🖼️", layout="centered")

# --- Custom CSS ---
st.markdown("""
<style>
.title { font-size:2.2em; font-weight:bold; color:#4CAF50; text-align:center; margin-bottom:10px; }
.subtitle { font-size:1.1em; color:#555; text-align:center; margin-bottom:30px; }
.footer { text-align:center; color:gray; font-size:0.9em; margin-top:50px; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<p class="title">🖼️ AI Image Captioning App</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload an image and let AI generate a smart caption for you!</p>', unsafe_allow_html=True)

# --- Load API Key from Streamlit Secrets ---
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
client = OpenAI()

# --- Upload Section ---
uploaded_file = st.file_uploader("📤 Step 1: Upload Your Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    if image.mode == "RGBA":
        image = image.convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Convert image to base64 (for display/log purposes if needed)
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    # --- User Prompt ---
    user_prompt = st.text_input("✍️ Step 2: Enter Your Prompt", "Give a creative caption for this image")

    if st.button("🚀 Generate Caption"):
        if user_prompt.strip() == "":
            st.warning("Please enter a prompt for the caption!")
        else:
            with st.spinner("AI is generating a caption... ⏳"):
                try:
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are an expert in image captioning. Provide detailed captions including objects, text, colors, context, and relationships."
                            },
                            {
                                "role": "user",
                                "content": f"{user_prompt}\n[IMAGE DATA: data:image/jpeg;base64,{b64}]"
                            }
                        ],
                        max_tokens=200
                    )
                    caption = resp.choices[0].message.content.strip()
                    st.markdown("### 📝 Generated Caption")
                    st.success(caption)
                except Exception as e:
                    st.error(f"Error generating caption: {e}")
else:
    st.info("👆 Upload an image to get started.")

# --- Footer ---
st.markdown('<p class="footer">Built with ❤️ using Streamlit & OpenAI</p>', unsafe_allow_html=True)
