@echo off
cd /d D:\llama
llama-cli.exe -m "D:\llama\models\Qwen_Qwen3-8B-Q4_K_M.gguf" -p "Explain cloud computing in simple words." -n 200 --reasoning off
pause
