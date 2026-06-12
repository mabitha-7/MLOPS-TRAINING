import streamlit as st
from ultralytics import YOLO
from PIL import Image
import tempfile
import os
import subprocess

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Ship Hull Biofouling Detection",
    page_icon="🚢",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main-title{
    text-align:center;
    font-size:60px;
    font-weight:bold;
    color:#00BFFF;
}
.sub-title{
    text-align:center;
    font-size:24px;
    color:white;
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown(
    '<div class="main-title">🚢 Ship Hull Biofouling Detection</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">AI Powered Marine Growth Detection using YOLOv8</div>',
    unsafe_allow_html=True
)

# ---------------- MODEL ----------------
@st.cache_resource
def load_model():
    return YOLO("best.pt")

model = load_model()

st.success("✅ YOLO Model Loaded Successfully")

# =====================================================
# IMAGE DETECTION
# =====================================================
st.header("📷 Image Detection")

uploaded_file = st.file_uploader(
    "Upload Ship Hull Image",
    type=["jpg", "jpeg", "png"],
    key="image_upload"
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Uploaded Image")
        st.image(
            image,
            use_container_width=True
        )

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    ) as tmp:
        uploaded_file.seek(0)
        tmp.write(uploaded_file.read())
        image_path = tmp.name

    if st.button(
        "🔍 Detect Image Biofouling",
        use_container_width=True
    ):
        with st.spinner(
            "Running AI Detection..."
        ):
            results = model.predict(
                source=image_path,
                conf=0.25
            )

            annotated_image = results[0].plot()

            with col2:
                st.subheader(
                    "Detection Result"
                )
                st.image(
                    annotated_image,
                    use_container_width=True
                )

            boxes = results[0].boxes

            st.markdown("---")

            if len(boxes) > 0:
                class_id = int(
                    boxes[0].cls[0]
                )
                confidence = float(
                    boxes[0].conf[0]
                )
                class_name = model.names[
                    class_id
                ]

                m1, m2, m3 = st.columns(3)

                with m1:
                    st.metric(
                        "Class",
                        class_name
                    )

                with m2:
                    st.metric(
                        "Confidence",
                        f"{confidence:.2f}"
                    )

                with m3:
                    st.metric(
                        "Objects",
                        len(boxes)
                    )

                if class_name == "clean_hull":
                    st.success(
                        "✅ Hull Surface is Clean"
                    )
                elif class_name == "marine_growth":
                    st.warning(
                        "⚠ Marine Growth Detected"
                    )
                elif class_name == "heavy_marine_growth":
                    st.error(
                        "🚨 Heavy Marine Growth Detected"
                    )
            else:
                st.warning(
                    "⚠ No Marine Growth Detected"
                )

    try:
        os.remove(image_path)
    except:
        pass

# =====================================================
# VIDEO DETECTION
# =====================================================
st.markdown("---")
st.header("🎥 Video Detection")

video_file = st.file_uploader(
    "Upload Ship Hull Video",
    type=["mp4", "avi", "mov"],
    key="video_upload"
)

if video_file is not None:
    st.subheader("Uploaded Video")
    st.video(video_file)

    if st.button(
        "🎯 Detect Video Biofouling",
        use_container_width=True
    ):
        with st.spinner(
            "Processing Video..."
        ):
            # Ensure uploads directory exists
            if not os.path.exists("uploads"):
                os.makedirs("uploads")
                
            video_path = os.path.join(
                "uploads",
                video_file.name
            )

            with open(
                video_path,
                "wb"
            ) as f:
                f.write(
                    video_file.getbuffer()
                )

            results = model.predict(
                source=video_path,
                save=True,
                conf=0.25
            )

            detect_path = "runs/detect"

            predict_folders = [
                os.path.join(
                    detect_path,
                    d
                )
                for d in os.listdir(
                    detect_path
                )
                if d.startswith(
                    "predict"
                )
            ]

            latest_folder = max(
                predict_folders,
                key=os.path.getmtime
            )

            output_video = None

            for file in os.listdir(
                latest_folder
            ):
                if file.endswith(
                    ".avi"
                ) or file.endswith(
                    ".mp4"
                ):
                    output_video = os.path.join(
                        latest_folder,
                        file
                    )
                    break

            st.success(
                "✅ Video Processing Completed"
            )

            # --- FFmpeg Integration for Streamlit Playback ---
            if output_video:
                ffmpeg_path = r"G:\ffmpeg\ffmpeg-8.1.1-essentials_build\bin\ffmpeg.exe"
                mp4_output = output_video.replace(".avi", "_streamlit.mp4")

                if output_video.endswith(".avi"):
                    with st.spinner("Converting video format for web player..."):
                        subprocess.run(
                            [
                                ffmpeg_path,
                                "-i", output_video,
                                "-vcodec", "libx264",
                                "-acodec", "aac",
                                "-y",
                                mp4_output
                            ]
                        )
                    output_video = mp4_output

                st.subheader(
                    "Processed Video"
                )
                st.video(output_video)

                detection_found = False

                for r in results:
                    if len(
                        r.boxes
                    ) > 0:
                        detection_found = True
                        break

                if detection_found:
                    st.error(
                        "🚨 Heavy Marine Growth Detected In Video"
                    )
                else:
                    st.success(
                        "✅ No Marine Growth Detected"
                    )
            else:
                st.warning(
                    "⚠ Processed video not found"
                )