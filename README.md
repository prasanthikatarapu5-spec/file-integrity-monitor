# 🔐 File Integrity Monitor

A simple Python-based cybersecurity tool that detects unexpected changes to files using SHA-256 hashing.

## 📌 What is File Integrity Monitoring?

File Integrity Monitoring (FIM) is a security technique used to detect unexpected changes to important files.

This project creates a baseline of file hashes and compares them later to identify changes.

## 🚀 Features

- ✅ Detect unchanged files
- ⚠️ Detect modified files
- ❌ Detect deleted files
- 🆕 Detect newly added files
- 📊 Display a security summary
- 🔐 Uses SHA-256 hashing
- 💻 Simple command-line interface
- 🐍 Built using Python standard libraries

## 🛠️ Technologies Used

- Python 3
- SHA-256
- JSON
- File System Operations

## 📂 Project Structure

```text
file-integrity-monitor/
│
├── main.py
├── .gitignore
├── README.md
└── test_files/
    ├── config.txt
    ├── test.txt
    └── secret.txt
