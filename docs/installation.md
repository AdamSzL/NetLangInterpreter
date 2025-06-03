# 📦 NetLang – Installation & Usage Guide

This document explains how to install and run the NetLang interpreter.

---

## ✅ Requirements

- Python 3.8 or higher
- Supported Operating Systems:
  - ✅ Linux
  - ✅ macOS
  - ✅ Windows

---

## 📥 Cloning the Project

```bash
git clone https://github.com/AdamSzL/NetLangInterpreter.git
cd NetLangInterpreter
```

---

## 🧪 Installing Dependencies

Make sure you have all required Python packages installed. You can install them using:

### Option 1: Global installation

```bash
pip install -r requirements.txt
```

### Option 2: Virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶️ Running the Interpreter (Basic Python Usage)

You can run the interpreter directly using Python:

1. Linux/macOS

    ```bash
    python main.py examples/star_topology.netlang
    ```
   
2. Windows

    ```bash
    python main.py examples\star_topology.netlang
    ```

---

## 🚀 Running NetLang programs with the `nlg` command

To simplify execution, NetLang provides launcher scripts for Unix and Windows.

### Linux/macOS

1. Grant execution permissions:

   ```bash
   chmod +x nlg
   ```

2. (Optional) Install globally:

   ```bash
   sudo cp nlg /usr/local/bin/nlg
   ```

3. Run:

   ```bash
   nlg examples/star_topology.netlang
   ```

---

### Windows

1. Run:

   ```cmd
   nlg examples\star_topology.netlang
   ```

2. *(Optional)* To run `nlg` from any directory:
   - Add the project folder to your system `PATH`, or
   - Copy `nlg.bat` to a directory already in `PATH` (e.g., `C:\Windows\System32`)

---

## ℹ️ Need Help?

If you encounter any problems:
- Refer to the main [README.md](../README.md)
- Open an issue on GitHub