# Local Mind Bridge

Run a local GGUF large language model from your laptop using **llama.cpp**, expose it through **llama-server**, wrap it with a small **Python Flask API**, and access it from both a **web browser** and a **Flutter mobile app**.

This repository contains the lab guide, Flask wrapper program, Flutter client code, Windows command scripts, screenshots, and demo videos.

> The GGUF model file is **not included** because model files are usually several GB. Download the model separately and place it in your local `models` folder.

---

## 1. Lab Architecture

```text
User / Student
   |
   | Browser or Flutter mobile app
   v
Python Flask Wrapper
http://<laptop-ip>:5000
   |
   | OpenAI-compatible JSON request
   v
llama-server
http://127.0.0.1:8080/v1/chat/completions
   |
   v
Local GGUF Model
Qwen_Qwen3-8B-Q4_K_M.gguf
```

The lab demonstrates that a local AI model can run on a normal laptop without depending on cloud AI APIs.

---

## 2. Repository Contents

```text
local-llm-mobile-web-lab/
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── LAB_GUIDE.md
│   ├── GITHUB_UPLOAD_GUIDE.md
│   └── original_lab_study.docx
├── flask_wrapper/
│   ├── app.py
│   └── requirements.txt
├── flutter_app/
│   ├── lib/main.dart
│   └── android/app/src/main/AndroidManifest.xml
├── scripts/
│   ├── 01_test_llama_cli.bat
│   ├── 02_start_llama_server_local.bat
│   ├── 03_start_llama_server_lan.bat
│   ├── 04_start_flask_wrapper.bat
│   └── 05_test_api_curl.bat
└── media/
    ├── screenshots/
    ├── videos/
    └── video_frames/
```

---

## 3. Required Software

Install the following before running the lab:

1. **Windows 10/11**
2. **Python 3.10+**
3. **Flutter SDK**
4. **llama.cpp Windows release**
5. A downloaded **GGUF model**, for example:
   - `Qwen_Qwen3-8B-Q4_K_M.gguf`

Recommended local folders:

```text
D:\llama
D:\llama\models
```

Put the downloaded model here:

```text
D:\llama\models\Qwen_Qwen3-8B-Q4_K_M.gguf
```

---

## 4. Quick Start

### Step 1: Start llama-server

Open Command Prompt in `D:\llama`:

```cmd
llama-server.exe -m "D:\llama\models\Qwen_Qwen3-8B-Q4_K_M.gguf" --host 127.0.0.1 --port 8080 --reasoning off
```

Keep this window open.

### Step 2: Start the Flask wrapper

Open another Command Prompt inside this repository:

```cmd
cd flask_wrapper
pip install -r requirements.txt
python app.py
```

Open the help page:

```text
http://127.0.0.1:5000/
```

From another device on the same Wi-Fi, use the laptop IP address:

```text
http://192.168.100.39:5000/
```

Replace `192.168.100.39` with your real laptop IP address.

### Step 3: Ask from browser

```text
http://127.0.0.1:5000/ask?q=What is cloud computing?&format=html
```

For JSON:

```text
http://127.0.0.1:5000/ask?q=What is cloud computing?&format=json
```

### Step 4: Run Flutter app

Create a Flutter project or copy the provided `main.dart` into your own Flutter project.

```cmd
flutter create llama_mobile_app
cd llama_mobile_app
flutter pub add http
```

Then replace:

```text
lib/main.dart
```

with the file provided in this repository:

```text
flutter_app/lib/main.dart
```

Also add the Internet permission and cleartext setting from:

```text
flutter_app/android/app/src/main/AndroidManifest.xml
```

Run:

```cmd
flutter run
```

---

## 5. Important Notes

### Use JSON for mobile apps

The Flutter app must call:

```text
/ask?q=your question&format=json
```

or:

```text
/ask?q=your question&mobile=1
```

Otherwise, it may receive HTML and fail to decode the response as JSON.

### Same Wi-Fi requirement

The phone and laptop must be connected to the same Wi-Fi network.

### Windows Firewall

Allow Python/Flask through Windows Firewall if the mobile phone cannot access the laptop.

### Model file not included

The model file is intentionally excluded from GitHub because it is too large. Download it separately from Hugging Face.

---

## 6. Expected Result

At the end of the lab, students should be able to:

- Run a quantized GGUF LLM locally.
- Use `llama-cli` for command-line inference.
- Use `llama-server` as a local AI API.
- Build a Flask wrapper around the local AI server.
- Return both HTML and JSON responses.
- Connect a Flutter mobile app to the local AI model through Wi-Fi.
- Measure prompt speed, generation speed, and token usage.

---

## 7. Suggested Student Deliverables

Students should submit:

1. Screenshot of `llama-cli` running a prompt.
2. Screenshot of `llama-server` running.
3. Screenshot of Flask help page.
4. Screenshot of Flask HTML answer page.
5. Screenshot of Flask JSON response.
6. Screenshot or video of the Flutter app receiving a response.
7. Short comparison between `--temp 0.2` and `--temp 0.9`.

---

## 8. Demo Evidence

Screenshots and videos are stored in:

```text
media/screenshots
media/videos
media/video_frames
```

They show successful execution of the command-line, browser, web wrapper, and mobile app parts.
