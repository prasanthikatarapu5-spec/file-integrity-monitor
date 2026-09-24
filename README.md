# 🔐 File Integrity Monitor

A lightweight cybersecurity tool that detects unauthorized file changes using **SHA-256 cryptographic hashing**.

## 📌 About

File Integrity Monitoring (FIM) is a security technique used to detect changes to important files.

This project creates a trusted baseline of files and compares their SHA-256 hashes during later scans.

It can detect:

- ✅ Unchanged files
- ⚠️ Modified files
- ❌ Deleted files
- 🆕 Newly created files

## 🚀 Features

- SHA-256 file hashing
- Baseline creation
- File modification detection
- File deletion detection
- New file detection
- Security summary
- Terminal security interface
- No external Python packages required

## 🛠️ Technologies

- Python
- SHA-256
- JSON
- File System Monitoring
- Git & GitHub

## 📂 Project Structure

```text
file-integrity-monitor/
│
├── main.py
├── README.md
├── .gitignore
│
└── test_files/
    ├── config.txt
    ├── secret.txt
    └── test.txt
