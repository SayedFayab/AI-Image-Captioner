import streamlit as st
from PIL import Image
import base64, io,os
from openai import OpenAI

# --- Page Config ---
st.set_page_config(
    page_title="AI Image Captioning",
    page_icon="🖼️",
    layout="centered",
)

# --- Custom CSS ---
st.markdown("""
    <style>
    .title {
        font-size: 2.2em;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 1.1em;
        color: #555;
        text-align: center;
        margin-bottom: 30px;
    }
    .footer {
        text-align: center;
        color: gray;
        font-size: 0.9em;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<p class="title">🖼️ AI Image Captioning App</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload an image and let AI generate a smart caption for you!</p>', unsafe_allow_html=True)
# Load API key
with open(r"C:\Users\fayab\Desktop\AI\GENAI\API_Keys\OPENAI_API_KEY.txt") as f:
    OPENAI_API_KEY = f.read().strip()
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

client = OpenAI()

# --- Upload Section ---
st.markdown("### 📤 Step 1: Upload Your Image")
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    # Ensure image is in RGB (JPEG doesn’t support RGBA)
    if image.mode == "RGBA":
        image = image.convert("RGB")

    # Convert to base64
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
      
    st.markdown("---")

    # --- User Prompt ---
    st.markdown("### ✍️ Step 2: Enter Your Prompt")
    user_prompt = st.text_input("Example: 'Give a creative caption for this image'")
    #Call GPT-4o model
    resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
            "role": "system",
            "content": "You are an expert in image captioning. Always provide detailed, accurate captions including objects, text, colors, context, and relationships don't be a poit just provide detailed captions for the image."
        },
                {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                ],
            }],
            max_tokens=100,
 )    


    # --- Process Button ---
    if st.button("🚀 Generate Caption"):
        with st.spinner("AI is generating a caption... ⏳"):
            # Call your model here (example placeholder)
            # Replace with your OpenAI API call
            caption = f"✨ [Demo Caption] Based on your prompt: {user_prompt}"  

            # --- Display Result ---
            st.markdown("### 📝 Generated Caption")
            st.success(caption)
            st.write(resp.choices[0].message.content.strip())

else:
    st.info("👆 Upload an image to get started.")

# --- Footer ---
st.markdown('<p class="footer">Built with ❤️ using Streamlit & OpenAI</p>', unsafe_allow_html=True)

