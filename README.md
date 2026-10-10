# 🔍 AI Image Detector

A web app that classifies uploaded images as **Real** or **AI-Generated** using a transfer-learning model built on MobileNetV2, trained on the CIFAKE dataset. Built with TensorFlow and deployed with Streamlit.

**🔗 Live Demo:** [ai-image-detector.streamlit.app](https://ai-image-detector-dabmnwcjuhvwhnk7bdvtpg.streamlit.app)

---

## 📌 Overview

With the rapid rise of AI-generated imagery (deepfakes, synthetic media, diffusion-model outputs), distinguishing real photos from AI-generated ones is becoming increasingly important for journalism, social platforms, and education. This project is a lightweight, beginner-friendly binary classifier that tackles this problem using transfer learning for fast, practical results.

## ✨ Features

- Upload any JPG/PNG image and get an instant prediction
- Real-time confidence score with a visual progress bar
- Clean, responsive Streamlit interface
- Fast inference using a frozen MobileNetV2 backbone

## 🛠️ Tech Stack

- **Model:** MobileNetV2 (transfer learning, ImageNet weights, frozen base)
- **Framework:** TensorFlow / Keras
- **Dataset:** [CIFAKE](https://www.kaggle.com/datasets/birdy654/cifake-real-and-ai-generated-synthetic-images) — 120K real vs. AI-generated images
- **Frontend:** Streamlit
- **Deployment:** Streamlit Community Cloud

## 📂 Project Structure

```
ai-image-detector/
├── app.py              # Streamlit app
├── detector.h5          # Trained model weights
├── requirements.txt     # Python dependencies
└── README.md
```

## 🚀 Run Locally

1. Clone the repository
   ```bash
   git clone https://github.com/jayanthvanjarapu0/ai-image-detector.git
   cd ai-image-detector
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app
   ```bash
   streamlit run app.py
   ```

## 🧠 Model Details

- **Architecture:** MobileNetV2 base (frozen) + GlobalAveragePooling2D + Dense(32, relu) + Dense(1, sigmoid)
- **Input size:** 96x96 RGB images
- **Training:** 4 epochs on a subset of the CIFAKE dataset
- **Output:** Binary classification (Real / AI-Generated) with confidence score

## ⚠️ Limitations

- Trained on a reduced dataset subset for fast iteration — accuracy can be improved with full-dataset training and fine-tuning
- Performance may vary on images from AI generators not represented in the CIFAKE training data (e.g., newer diffusion models)
- Not intended for forensic or legal use — a demonstration of the approach, not a production-grade detector

## 🔮 Future Improvements

- Fine-tune deeper layers of MobileNetV2 for higher accuracy
- Add Grad-CAM visualization to show which image regions influenced the prediction
- Expand training data to include more diverse AI generators
- Add example images for quick testing without an upload

## 👤 Author

**Jayanth Vanjarapu**
- GitHub: [@jayanthvanjarapu0](https://github.com/jayanthvanjarapu0)
- Email: jayanthvanjarapu0@gmail.com

## 📄 License

This project is open source and available under the MIT License.
