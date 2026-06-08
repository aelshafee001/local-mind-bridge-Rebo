# Lab Guide: Run a Local AI Model and Connect It to Web and Mobile Apps

## Objective

Run a local GGUF large language model from the hard disk using `llama.cpp`, then expose it through a local web/API service and connect it to a Flutter mobile app.

By the end of this lab, students will understand the complete deployment path:

```text
Local LLM model → llama.cpp → llama-server → Flask API → Browser / Flutter mobile app
```

---

## Part 1: Background Concepts

### What is a local LLM?

A local LLM is a large language model that runs directly on your own computer instead of depending on a cloud provider.

### What does 8B mean?

`8B` means the model has about 8 billion learned parameters. A parameter is a number learned during training. These parameters help the model generate text, answer questions, summarize, translate, and write code.

### What is GGUF?

GGUF is the model file format commonly used by `llama.cpp` and many local LLM tools.

### What is quantization?

Quantization reduces model weight precision, for example from 16-bit or 32-bit floating-point numbers into lower precision values such as 8-bit, 5-bit, or 4-bit values. This reduces model size and memory usage, but may slightly reduce quality.

Examples:

| Quantization | Meaning |
|---|---|
| Q4_K_S | 4-bit K-quant small variant |
| Q4_K_M | 4-bit K-quant medium variant |
| Q5_K_M | 5-bit K-quant medium variant |
| Q6_K | 6-bit quantization |
| Q8_0 | 8-bit quantization |

---

## Part 2: Prepare Folders

Create:

```cmd
mkdir D:\llama
mkdir D:\llama\models
```

Place your model file here:

```text
D:\llama\models\Qwen_Qwen3-8B-Q4_K_M.gguf
```

---

## Part 3: Download llama.cpp

1. Open the official llama.cpp releases page on GitHub.
2. Download the Windows prebuilt release.
3. Extract it into:

```text
D:\llama
```

You should have:

```text
D:\llama\llama-cli.exe
D:\llama\llama-server.exe
```

---

## Part 4: Test llama-cli

Open Command Prompt:

```cmd
cd /d D:\llama
llama-cli.exe --help
```

If help options appear, installation is correct.

---

## Part 5: Run a Prompt from Command Line

```cmd
llama-cli.exe -m "D:\llama\models\Qwen_Qwen3-8B-Q4_K_M.gguf" -p "Explain cloud computing in simple words." -n 200 --reasoning off
```

Expected result: the model should load and generate an answer.

---

## Part 6: Run Chat Mode

```cmd
llama-cli.exe -m "D:\llama\models\Qwen_Qwen3-8B-Q4_K_M.gguf" -cnv --reasoning off
```

Then type questions directly.

Useful commands inside chat mode:

| Command | Meaning |
|---|---|
| `/exit` | Stop or exit |
| `/regen` | Regenerate last response |
| `/clear` | Clear chat history |
| `/read <file>` | Add a text file |

---

## Part 7: Compare Temperature

Run the same prompt twice:

```cmd
llama-cli.exe -m "D:\llama\models\Qwen_Qwen3-8B-Q4_K_M.gguf" -p "Explain cloud computing in simple words." -n 200 --temp 0.2 --reasoning off
```

Then:

```cmd
llama-cli.exe -m "D:\llama\models\Qwen_Qwen3-8B-Q4_K_M.gguf" -p "Explain cloud computing in simple words." -n 200 --temp 0.9 --reasoning off
```

Expected comparison:

| Temperature | Expected Output |
|---|---|
| 0.2 | More stable, direct, predictable |
| 0.9 | More creative, varied, sometimes less controlled |

---

## Part 8: Run llama-server

Start local server:

```cmd
llama-server.exe -m "D:\llama\models\Qwen_Qwen3-8B-Q4_K_M.gguf" --host 127.0.0.1 --port 8080 --reasoning off
```

Open:

```text
http://127.0.0.1:8080
```

---

## Part 9: Test the API with curl

```cmd
curl http://127.0.0.1:8080/v1/chat/completions ^
-H "Content-Type: application/json" ^
-d "{\"messages\":[{\"role\":\"user\",\"content\":\"Explain cloud computing in simple words.\"}],\"temperature\":0.4,\"max_tokens\":200}"
```

---

## Part 10: Run the Flask Wrapper

Go to the Flask folder:

```cmd
cd flask_wrapper
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000/
```

Ask in browser:

```text
http://127.0.0.1:5000/ask?q=What is cloud computing?&format=html
```

Ask and receive JSON:

```text
http://127.0.0.1:5000/ask?q=What is cloud computing?&format=json
```

---

## Part 11: Access Flask from Mobile Phone

Find your laptop IP:

```cmd
ipconfig
```

Example:

```text
192.168.100.39
```

From the phone browser, open:

```text
http://192.168.100.39:5000/
```

The phone and laptop must be on the same Wi-Fi network.

---

## Part 12: Build Flutter App

```cmd
flutter create llama_mobile_app
cd llama_mobile_app
flutter pub add http
```

Replace `lib/main.dart` with the provided file:

```text
flutter_app/lib/main.dart
```

Edit the server URL inside the app or from the app text field:

```text
http://192.168.100.39:5000
```

Run:

```cmd
flutter run
```

---

## Part 13: Student Report Requirements

Students should include:

1. Command used to run `llama-cli`.
2. Screenshot of successful local model answer.
3. Command used to start `llama-server`.
4. Screenshot of Flask help page.
5. Screenshot of Flask HTML answer.
6. Screenshot of JSON response.
7. Screenshot or video of Flutter app result.
8. Table comparing temperature 0.2 and 0.9.
9. Observed generation speed.

---

## Troubleshooting

### Mobile cannot connect

Check:

1. Laptop and phone are on the same Wi-Fi.
2. Flask is running on `0.0.0.0`.
3. Windows Firewall allows Python.
4. Correct laptop IP is used.
5. URL includes port `5000`.

### Flutter JSON error

Use:

```text
/ask?q=your question&format=json
```

Do not use HTML format for mobile JSON decoding.

### Model shows reasoning text

Start the model with:

```cmd
--reasoning off
```

### Model is slow

Try:

- Smaller model, such as 3B or 4B.
- Smaller `max_tokens`.
- Lower context size.
- More RAM or GPU acceleration if available.
