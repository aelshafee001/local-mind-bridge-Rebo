@echo off
curl http://127.0.0.1:8080/v1/chat/completions ^
-H "Content-Type: application/json" ^
-d "{\"messages\":[{\"role\":\"user\",\"content\":\"Explain cloud computing in simple words.\"}],\"temperature\":0.4,\"max_tokens\":200}"
pause
