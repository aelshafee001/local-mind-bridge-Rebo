# How to Upload and Build This Lab on GitHub

This guide explains two simple methods: uploading through the GitHub website and uploading using Git commands.

---

## Method 1: Upload Using GitHub Website

### Step 1: Create a new repository

1. Open GitHub.
2. Click **New repository**.
3. Repository name suggestion:

```text
local-llm-mobile-web-lab
```

4. Add a description:

```text
A practical lab for running a local GGUF LLM with llama.cpp and connecting it to web and Flutter mobile clients.
```

5. Choose **Public** or **Private**.
6. Do not add another README if you will upload this repository folder.
7. Click **Create repository**.

---

### Step 2: Upload the files

1. Open the new empty repository.
2. Click **uploading an existing file**.
3. Drag all files and folders from this repository into the upload area.
4. Wait until the files finish uploading.
5. Write commit message:

```text
Initial lab repository with Flask wrapper, Flutter client, scripts, and media
```

6. Click **Commit changes**.

---

## Method 2: Upload Using Git Commands

### Step 1: Install Git

Download and install Git for Windows if it is not already installed.

### Step 2: Open Command Prompt in the repository folder

Example:

```cmd
cd local-llm-mobile-web-lab
```

### Step 3: Initialize Git

```cmd
git init
```

### Step 4: Add files

```cmd
git add .
```

### Step 5: Commit files

```cmd
git commit -m "Initial lab repository"
```

### Step 6: Connect to GitHub repository

After creating the GitHub repository, copy its URL. Then run:

```cmd
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/local-llm-mobile-web-lab.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## Important GitHub Notes

### Do not upload GGUF model files

Model files are usually several GB and should not be uploaded to GitHub.

This repository already includes `.gitignore` rules:

```text
*.gguf
models/
```

### Video files

GitHub allows files up to 100 MB each. The included demo videos are below that limit. If you later add larger videos, use one of these options:

- Compress the video.
- Upload it to YouTube or Google Drive and place the link in the README.
- Use Git LFS for large files.

---

## Recommended Repository Settings

After uploading, edit the repository About section:

**Description**:

```text
Run a local GGUF LLM using llama.cpp and connect it to Flask, browser, and Flutter mobile app.
```

**Topics**:

```text
llama-cpp, gguf, local-llm, flask, flutter, ai-lab, mobile-app, python
```

---

## Suggested GitHub README Preview Sections

The README should show:

1. Lab objective.
2. Architecture diagram.
3. Requirements.
4. Quick start commands.
5. Screenshots and videos.
6. Student tasks.
7. Troubleshooting.

These sections are already included in the provided `README.md`.
