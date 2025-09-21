# Movie Recommendation System - PowerShell Launcher
# Run this script to launch the movie recommendation system

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    Movie Recommendation System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

function Show-Menu {
    Write-Host "Choose an option:" -ForegroundColor Yellow
    Write-Host "1. Install dependencies" -ForegroundColor White
    Write-Host "2. Test system (check for errors)" -ForegroundColor White
    Write-Host "3. Run demo script" -ForegroundColor White
    Write-Host "4. Run web application" -ForegroundColor White
    Write-Host "5. Open Jupyter notebook" -ForegroundColor White
    Write-Host "6. Check Python installation" -ForegroundColor White
    Write-Host "7. Exit" -ForegroundColor White
    Write-Host ""
}

function Install-Dependencies {
    Write-Host "Installing dependencies..." -ForegroundColor Green
    try {
        $result = pip install -r requirements.txt 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Dependencies installed successfully!" -ForegroundColor Green
        } else {
            Write-Host "Error installing dependencies. Please check if Python and pip are installed." -ForegroundColor Red
            Write-Host "You can download Python from: https://python.org" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "Error installing dependencies: $_" -ForegroundColor Red
    }
    Read-Host "Press Enter to continue"
}

function Test-System {
    Write-Host "Testing the system..." -ForegroundColor Green
    try {
        $result = python test_system.py 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "System test completed successfully!" -ForegroundColor Green
        } else {
            Write-Host "System test failed. Please check the error messages above." -ForegroundColor Red
        }
    }
    catch {
        Write-Host "Error running system test: $_" -ForegroundColor Red
    }
    Read-Host "Press Enter to continue"
}

function Run-Demo {
    Write-Host "Running demo script..." -ForegroundColor Green
    try {
        $result = python demo.py 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Demo failed. Please check the error messages above." -ForegroundColor Red
        }
    }
    catch {
        Write-Host "Error running demo: $_" -ForegroundColor Red
        Write-Host "Make sure Python is installed and in your PATH" -ForegroundColor Yellow
    }
    Read-Host "Press Enter to continue"
}

function Run-WebApp {
    Write-Host "Starting web application..." -ForegroundColor Green
    try {
        streamlit run src/web_app.py
    }
    catch {
        Write-Host "Error starting web app: $_" -ForegroundColor Red
        Write-Host "Make sure Streamlit is installed: pip install streamlit" -ForegroundColor Yellow
    }
}

function Open-Notebook {
    Write-Host "Opening Jupyter notebook..." -ForegroundColor Green
    try {
        jupyter notebook notebooks/movie_analysis.ipynb
    }
    catch {
        Write-Host "Error opening notebook: $_" -ForegroundColor Red
        Write-Host "Make sure Jupyter is installed: pip install jupyter" -ForegroundColor Yellow
    }
}

function Check-Python {
    Write-Host "Checking Python installation..." -ForegroundColor Green
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Python found: $pythonVersion" -ForegroundColor Green
        } else {
            Write-Host "Python not found in PATH" -ForegroundColor Red
            Write-Host "Please install Python from https://python.org" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "Python not found in PATH" -ForegroundColor Red
        Write-Host "Please install Python from https://python.org" -ForegroundColor Yellow
    }
    
    try {
        $pipVersion = pip --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Pip found: $pipVersion" -ForegroundColor Green
        } else {
            Write-Host "Pip not found" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "Pip not found" -ForegroundColor Red
    }
    
    Read-Host "Press Enter to continue"
}

# Main menu loop
do {
    Show-Menu
    $choice = Read-Host "Enter your choice (1-7)"
    
    switch ($choice) {
        "1" { Install-Dependencies }
        "2" { Test-System }
        "3" { Run-Demo }
        "4" { Run-WebApp }
        "5" { Open-Notebook }
        "6" { Check-Python }
        "7" { 
            Write-Host "Thank you for using Movie Recommendation System!" -ForegroundColor Cyan
            break 
        }
        default { 
            Write-Host "Invalid choice! Please enter a number between 1 and 7." -ForegroundColor Red
            Read-Host "Press Enter to continue"
        }
    }
    
    Clear-Host
} while ($true)
