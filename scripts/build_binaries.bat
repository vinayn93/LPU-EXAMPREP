@echo off
echo =======================================================
echo   Building LPU ExamPrep C++ and C Native Executables
echo =======================================================

cd /d "%~dp0.."

echo [1/2] Compiling C++ Study Planner Engine (g++)...
g++ -O3 -std=c++17 cpp_planner/study_planner_engine.cpp -o cpp_planner/study_planner_engine.exe
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] C++ compilation failed.
    exit /b %ERRORLEVEL%
)
echo [SUCCESS] C++ binary generated: cpp_planner/study_planner_engine.exe

echo [2/2] Compiling C Academic Data Manager (gcc)...
gcc -O2 c_data_manager/exam_data_manager.c -o c_data_manager/exam_data_manager.exe
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] C compilation failed.
    exit /b %ERRORLEVEL%
)
echo [SUCCESS] C binary generated: c_data_manager/exam_data_manager.exe

echo =======================================================
echo   All LPU ExamPrep Native Binaries Built Successfully!
echo =======================================================
