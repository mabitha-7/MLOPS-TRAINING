# 🚢 Ship Hull Biofouling Detection using YOLOv8

## 📌 Project Overview

Ship hull biofouling is the accumulation of marine organisms such as algae, barnacles, and other aquatic species on the surface of a ship's hull. Excessive biofouling increases fuel consumption, maintenance costs, and environmental impact.

This project uses a custom-trained YOLOv8 object detection model to automatically detect marine growth on ship hull surfaces from both images and videos.

A Streamlit web application is developed to provide an easy-to-use interface for biofouling inspection.

---

## 🎯 Objective

* Detect marine growth on ship hull surfaces.
* Classify hull conditions using AI.
* Analyze both images and videos.
* Provide a user-friendly web interface using Streamlit.

---

## 🛠 Technologies Used

* Python
* YOLOv8 (Ultralytics)
* OpenCV
* Streamlit
* Pillow (PIL)
* FFmpeg
* NumPy

---

## 📂 Dataset Preparation

### Data Collection

* Ship hull inspection videos collected from marine inspection sources.

### Frame Extraction

* Video frames extracted using FFmpeg/OpenCV.

### Annotation

* Images manually annotated using bounding boxes.

### Dataset Structure

yolo_dataset/

├── images/

│   ├── train/

│   ├── valid/

│   └── test/

│

└── labels/

├── train/

├── valid/

└── test/

---

## 🏷 Classes

| Class Name          | Description             |
| ------------------- | ----------------------- |
| clean_hull          | Clean ship hull surface |
| marine_growth       | Moderate marine growth  |
| heavy_marine_growth | Heavy marine growth     |

---

## 🤖 Model Training

YOLOv8 custom object detection model was trained using the prepared dataset.

### Training Command

```bash
yolo detect train data=data.yaml model=yolov8n.pt epochs=50 imgsz=640
```

### Output

```text
best.pt
```

The trained model weights are stored in:

```text
runs/detect/train/weights/best.pt
```

---

## 📷 Image Detection Workflow

1. Upload image.
2. YOLO model performs inference.
3. Bounding boxes are drawn.
4. Class and confidence score displayed.
5. Hull condition reported.

---

## 🎥 Video Detection Workflow

1. Upload video.
2. YOLO processes each frame.
3. Bounding boxes generated.
4. Output video saved.
5. FFmpeg converts AVI to MP4.
6. Processed video displayed in Streamlit.

---

## 🌐 Streamlit Application Features

### Image Detection

* Upload JPG/PNG images.
* Detect marine growth.
* Display confidence scores.
* Show bounding boxes.

### Video Detection

* Upload MP4/AVI/MOV videos.
* Process complete video.
* Display annotated video.
* Generate inspection results.

---

## 📁 Project Structure

ship-hull-biofouling-inspection/

├── raw_videos/

├── uploads/

├── yolo_dataset/

├── runs/

├── best.pt

├── streamlit_app.py

├── requirements.txt

└── README.md

---

## ▶️ Run the Application

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Launch Streamlit

```bash
python -m streamlit run streamlit_app.py
```

---

## 📊 Results

### Image Detection

* Accurate detection of marine growth.
* Bounding box visualization.
* Confidence score reporting.

### Video Detection

* Frame-by-frame biofouling inspection.
* Annotated output video generation.
* Browser-compatible MP4 playback.

---

## ⚠ Challenges Faced

* Large video processing time.
* Streamlit AVI playback issue.
* FFmpeg integration.
* Output video conversion.
* Managing YOLO inference results.

---

## ✅ Solutions Implemented

* Converted AVI output to MP4 using FFmpeg.
* Optimized Streamlit workflow.
* Added image and video detection modules.
* Improved user interface and reporting.

---

## 🚀 Future Enhancements

* Real-time ship inspection.
* Cloud deployment.
* Detection analytics dashboard.
* Downloadable inspection reports.
* Multi-class marine growth analysis.

---

## 👨‍💻 Author

Mabitha M

AI & Machine Learning Project

Ship Hull Biofouling Detection using YOLOv8 and Streamlit
