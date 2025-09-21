# 🛠️ Troubleshooting Guide - Movie Recommendation System

## 🚨 Common Issues and Solutions

### 1. **Python Not Found Error**

**Problem**: `Python was not found; run without arguments to install from the Microsoft Store`

**Solution**:
1. **Download Python** from [python.org](https://python.org)
2. **During installation**, make sure to check "Add Python to PATH"
3. **Restart** your command prompt/PowerShell
4. **Verify installation**: `python --version`

**Alternative**: If you prefer Microsoft Store version, search for "Python" and install it.

---

### 2. **Import Errors**

**Problem**: `ModuleNotFoundError: No module named 'data_processing'`

**Solution**:
1. **Make sure you're in the project root directory**
2. **Run the test script first**: `python test_system.py`
3. **Check file structure** - ensure `src/` folder contains all Python files
4. **Verify Python path**: The system should automatically add `src/` to your Python path

---

### 3. **Dependencies Installation Errors**

**Problem**: `pip install -r requirements.txt` fails

**Solution**:
1. **Update pip**: `python -m pip install --upgrade pip`
2. **Install dependencies one by one**:
   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn
   pip install requests beautifulsoup4 streamlit plotly jupyter
   ```
3. **Check Python version**: Ensure you have Python 3.8 or higher
4. **Use virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

---

### 4. **Streamlit Won't Start**

**Problem**: `streamlit run src/web_app.py` fails

**Solution**:
1. **Install Streamlit**: `pip install streamlit`
2. **Check port availability**: Streamlit uses port 8501 by default
3. **Try different port**: `streamlit run src/web_app.py --server.port 8502`
4. **Check firewall**: Ensure port 8501 is not blocked

---

### 5. **Jupyter Notebook Issues**

**Problem**: `jupyter notebook` command not found

**Solution**:
1. **Install Jupyter**: `pip install jupyter notebook`
2. **Alternative**: Use VS Code with Python extension
3. **Check installation**: `jupyter --version`

---

### 6. **Memory or Performance Issues**

**Problem**: System runs slowly or crashes

**Solution**:
1. **Close other applications** to free up memory
2. **Reduce dataset size** (the sample data is small, so this shouldn't be an issue)
3. **Check available RAM**: Ensure you have at least 4GB free
4. **Use virtual environment** to avoid conflicts

---

### 7. **File Path Issues**

**Problem**: Files not found or wrong directory

**Solution**:
1. **Verify project structure**:
   ```
   PROJECT/
   ├── src/
   │   ├── __init__.py
   │   ├── data_processing.py
   │   ├── recommendation.py
   │   ├── imdb_scraper.py
   │   └── web_app.py
   ├── demo.py
   ├── test_system.py
   └── requirements.txt
   ```
2. **Run from project root**: Always run commands from the main PROJECT folder
3. **Use absolute paths** if needed

---

### 8. **Web Browser Issues**

**Problem**: Web app opens but doesn't work properly

**Solution**:
1. **Clear browser cache** and cookies
2. **Try different browser** (Chrome, Firefox, Edge)
3. **Check browser console** for JavaScript errors
4. **Disable browser extensions** temporarily

---

## 🔍 **Diagnostic Steps**

### **Step 1: Check Python Installation**
```bash
python --version
pip --version
```

### **Step 2: Test Basic Imports**
```bash
python test_system.py
```

### **Step 3: Check Dependencies**
```bash
pip list | findstr pandas
pip list | findstr streamlit
```

### **Step 4: Verify File Structure**
```bash
dir src
dir *.py
```

---

## 🆘 **Getting Help**

### **Before Asking for Help**:
1. ✅ **Run the test script**: `python test_system.py`
2. ✅ **Check Python version**: `python --version`
3. ✅ **Verify dependencies**: `pip list`
4. ✅ **Check error messages** carefully
5. ✅ **Try the launcher scripts**: `run_project.bat` or `run_project.ps1`

### **When Asking for Help, Include**:
- **Error message** (copy and paste exactly)
- **Python version**: `python --version`
- **Operating system**: Windows/Mac/Linux
- **What you were trying to do**
- **Output of**: `python test_system.py`

---

## 🚀 **Quick Fixes**

### **If Nothing Works**:
1. **Delete and recreate virtual environment**:
   ```bash
   rmdir /s venv
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Reinstall Python**:
   - Uninstall Python completely
   - Download fresh copy from python.org
   - Install with "Add to PATH" checked

3. **Use the launcher scripts**:
   - Double-click `run_project.bat` (Windows)
   - Right-click `run_project.ps1` → "Run with PowerShell"

---

## ✅ **Success Indicators**

Your system is working correctly when:
- ✅ `python test_system.py` runs without errors
- ✅ `python demo.py` shows movie recommendations
- ✅ `streamlit run src/web_app.py` opens web interface
- ✅ `jupyter notebook` opens in browser

---

## 🎯 **Still Having Issues?**

1. **Check the error messages** - they often contain the solution
2. **Try running commands one by one** instead of using launchers
3. **Verify you're in the correct directory**
4. **Ensure all files are present** and not corrupted
5. **Check Windows Defender** or antivirus isn't blocking Python

**Remember**: The system is designed to work out-of-the-box. If you're still having issues, it's likely a Python installation or environment problem that can be easily resolved! 🎬✨
