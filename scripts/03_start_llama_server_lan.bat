@echo off
cd /d D:\llama
llama-server.exe -m "D:\llama\models\Qwen_Qwen3-8B-Q4_K_M.gguf" --host 0.0.0.0 --port 8080 --reasoning off
pause
