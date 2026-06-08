from flask import Flask, request, jsonify
import requests
import html

app = Flask(__name__)

# llama-server endpoint. Keep this local because Flask and llama-server run on the same laptop.
LLAMA_SERVER_URL = "http://127.0.0.1:8080/v1/chat/completions"


@app.route("/favicon.ico")
def favicon():
    return "", 204


def help_screen():
    return """
    <html>
        <head>
            <title>Local LLM Wrapper Help</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                pre { background: #f2f2f2; padding: 12px; border-radius: 8px; overflow-x: auto; }
                input[type=text] { width: 80%; padding: 10px; margin: 6px 0; }
                button { padding: 10px 18px; cursor: pointer; }
                table { border-collapse: collapse; }
                td, th { border: 1px solid #999; padding: 8px; }
            </style>
        </head>
        <body>
            <h2>Local LLM Wrapper Help</h2>

            <p>
                This server receives a question from the URL, sends it to
                <b>llama-server</b>, and returns the answer either as
                <b>HTML</b> for web browsers or <b>JSON</b> for mobile apps.
            </p>

            <h3>Quick Browser Test</h3>
            <form action="/ask" method="get">
                <input type="text" name="q" placeholder="Type your question here" value="What is cloud computing?" />
                <input type="hidden" name="format" value="html" />
                <button type="submit">Ask as HTML</button>
            </form>

            <h3>1. Ask a question and show answer in browser</h3>
            <pre>http://127.0.0.1:5000/ask?q=What is cloud computing?&format=html</pre>
            <p>Example:</p>
            <a href="/ask?q=What is cloud computing?&format=html">
                Ask: What is cloud computing? as HTML
            </a>

            <h3>2. Ask a question and receive JSON for Flutter/mobile</h3>
            <pre>http://127.0.0.1:5000/ask?q=What is cloud computing?&format=json</pre>
            <p>Example:</p>
            <a href="/ask?q=What is cloud computing?&format=json">
                Ask: What is cloud computing? as JSON
            </a>

            <h3>3. Using mobile flag</h3>
            <pre>http://127.0.0.1:5000/ask?q=What is AI?&mobile=1</pre>
            <p>If <code>mobile=1</code> is used, the server automatically returns JSON.</p>

            <h3>4. From another device on the same Wi-Fi</h3>
            <p>Replace <code>127.0.0.1</code> with your laptop IP address.</p>
            <pre>http://192.168.100.39:5000/ask?q=What is cloud computing?&format=json</pre>

            <h3>5. Required running services</h3>
            <p>First, run llama-server:</p>
            <pre>llama-server.exe -m "D:\\llama\\models\\Qwen_Qwen3-8B-Q4_K_M.gguf" --host 127.0.0.1 --port 8080 --reasoning off</pre>

            <p>Second, run this Flask wrapper:</p>
            <pre>python app.py</pre>

            <h3>6. Parameters</h3>
            <table>
                <tr><th>Parameter</th><th>Meaning</th><th>Example</th></tr>
                <tr><td>q</td><td>The question sent to the local LLM</td><td>q=What is AI?</td></tr>
                <tr><td>format</td><td>Output type: html or json</td><td>format=json</td></tr>
                <tr><td>mobile</td><td>If mobile=1, output will be JSON</td><td>mobile=1</td></tr>
            </table>
        </body>
    </html>
    """


@app.get("/")
def home():
    return help_screen()


def call_llama(question: str):
    payload = {
        "messages": [
            {
                "role": "user",
                "content": question + "\nGive the final answer only. Do not show reasoning."
            }
        ],
        "temperature": 0.4,
        "max_tokens": 500
    }

    response = requests.post(
        LLAMA_SERVER_URL,
        json=payload,
        timeout=180
    )
    response.raise_for_status()
    data = response.json()

    message = data.get("choices", [{}])[0].get("message", {})
    answer = message.get("content", "").strip()

    if not answer:
        answer = (
            "The model returned no final answer. "
            "Try increasing max_tokens or run llama-server with reasoning disabled."
        )

    timings = data.get("timings", {})
    usage = data.get("usage", {})

    return {
        "question": question,
        "answer": answer,
        "model": data.get("model", ""),
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "total_tokens": usage.get("total_tokens"),
        "prompt_tokens_per_second": timings.get("prompt_per_second"),
        "generation_tokens_per_second": timings.get("predicted_per_second")
    }


@app.get("/ask")
def ask():
    question = request.args.get("q", "").strip()
    output_format = request.args.get("format", "html").strip().lower()
    mobile = request.args.get("mobile", "0").strip()

    if mobile == "1":
        output_format = "json"

    if not question:
        help_data = {
            "message": "No question provided.",
            "usage": {
                "html": "/ask?q=Your question here&format=html",
                "json": "/ask?q=Your question here&format=json",
                "mobile": "/ask?q=Your question here&mobile=1"
            },
            "examples": {
                "browser": "http://127.0.0.1:5000/ask?q=What is cloud computing?&format=html",
                "flutter": "http://127.0.0.1:5000/ask?q=What is cloud computing?&format=json"
            }
        }
        if output_format == "json":
            return jsonify(help_data), 400
        return help_screen(), 200

    try:
        result = call_llama(question)

        if output_format == "json":
            return jsonify(result)

        safe_question = html.escape(result["question"])
        safe_answer = html.escape(result["answer"])

        return f"""
        <html>
            <head>
                <title>Local LLM Answer</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                    .question {{ background:#f2f2f2; padding:15px; border-radius:8px; }}
                    .answer {{ background:#eaf4ff; padding:15px; border-radius:8px; white-space:pre-wrap; }}
                    table {{ border-collapse: collapse; }}
                    td {{ border: 1px solid #999; padding: 8px; }}
                </style>
            </head>
            <body>
                <h2>Local LLM Answer</h2>
                <h3>Question</h3>
                <div class="question">{safe_question}</div>

                <h3>Answer</h3>
                <div class="answer">{safe_answer}</div>

                <h3>Model Information</h3>
                <table>
                    <tr><td>Model</td><td>{html.escape(str(result['model']))}</td></tr>
                    <tr><td>Prompt tokens</td><td>{result['prompt_tokens']}</td></tr>
                    <tr><td>Completion tokens</td><td>{result['completion_tokens']}</td></tr>
                    <tr><td>Total tokens</td><td>{result['total_tokens']}</td></tr>
                    <tr><td>Prompt speed</td><td>{result['prompt_tokens_per_second']} tokens/sec</td></tr>
                    <tr><td>Generation speed</td><td>{result['generation_tokens_per_second']} tokens/sec</td></tr>
                </table>

                <br>
                <a href="/">Back to Help</a>
            </body>
        </html>
        """

    except requests.exceptions.ConnectionError:
        error_data = {
            "error": "Cannot connect to llama-server.",
            "details": "Make sure llama-server is running on http://127.0.0.1:8080",
            "start_command": 'llama-server.exe -m "D:\\llama\\models\\Qwen_Qwen3-8B-Q4_K_M.gguf" --host 127.0.0.1 --port 8080 --reasoning off'
        }
        if output_format == "json":
            return jsonify(error_data), 503
        return f"""
        <html>
            <body style="font-family: Arial; margin: 40px;">
                <h2>Cannot connect to llama-server</h2>
                <p>Make sure llama-server is running on:</p>
                <pre>http://127.0.0.1:8080</pre>
                <p>Start it using:</p>
                <pre>{html.escape(error_data['start_command'])}</pre>
                <br><a href="/">Back to Help</a>
            </body>
        </html>
        """, 503

    except requests.exceptions.Timeout:
        error_data = {
            "error": "The model took too long to respond.",
            "details": "Try reducing max_tokens or use a smaller model."
        }
        if output_format == "json":
            return jsonify(error_data), 504
        return """
        <html>
            <body style="font-family: Arial; margin: 40px;">
                <h2>Timeout</h2>
                <p>The model took too long to respond.</p>
                <p>Try reducing max_tokens or using a smaller model.</p>
                <br><a href="/">Back to Help</a>
            </body>
        </html>
        """, 504

    except Exception as e:
        error_data = {
            "error": "Unexpected error.",
            "details": str(e)
        }
        if output_format == "json":
            return jsonify(error_data), 500
        return f"""
        <html>
            <body style="font-family: Arial; margin: 40px;">
                <h2>Unexpected Error</h2>
                <pre>{html.escape(str(e))}</pre>
                <br><a href="/">Back to Help</a>
            </body>
        </html>
        """, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
