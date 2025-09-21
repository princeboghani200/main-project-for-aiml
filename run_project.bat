ru@echo off
echo ========================================
echo    Movie Recommendation System
echo ========================================
echo.
echo This script helps you run the movie recommendation system
echo.
echo Choose an option:
echo 1. Install dependencies
echo 2. Test system (check for errors)
echo 3. Run demo script
echo 4. Run web application
echo 5. Open Jupyter notebook
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto test
if "%choice%"=="3" goto demo
if "%choice%"=="4" goto webapp
if "%choice%"=="5" goto notebook
if "%choice%"=="6" goto exit
goto invalid

:install
echo.
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo Error installing dependencies. Please check if Python and pip are installed.
    echo You can download Python from: https://python.org
    pause
    goto menu
)
echo.
echo Dependencies installed successfully!
pause
goto menu

:test
echo.
echo Testing the system...
python test_system.py
if %errorlevel% neq 0 (
    echo.
    echo System test failed. Please check the error messages above.
    pause
    goto menu
)
echo.
echo System test completed successfully!
pause
goto menu

:demo
echo.
echo Running demo script...
python demo.py
if %errorlevel% neq 0 (
    echo.
    echo Demo failed. Please check the error messages above.
    pause
    goto menu
)
echo.
pause
goto menu

:webapp
echo.
echo Starting web application...
streamlit run src/web_app.py
goto menu

:notebook
echo.
echo Opening Jupyter notebook...
jupyter notebook notebooks/movie_analysis.ipynb
goto menu

:invalid
echo.
echo Invalid choice! Please enter a number between 1 and 6.
pause
goto menu

:menu
cls
echo ========================================
echo    Movie Recommendation System
echo ========================================
echo.
echo Choose an option:
echo 1. Install dependencies
echo 2. Test system (check for errors)
echo 3. Run demo script
echo 4. Run web application
echo 5. Open Jupyter notebook
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto test
if "%choice%"=="3" goto demo
if "%choice%"=="4" goto webapp
if "%choice%"=="5" goto notebook
if "%choice%"=="6" goto exit
goto invalid

:exit
echo.
echo Thank you for using Movie Recommendation System!
pause
exit
