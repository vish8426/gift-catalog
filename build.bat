@echo off
REM ======================================================
REM Synthwave Gift Catalog - Build Script
REM Author: vish
REM Description: Builds a Onefile .exe with Custom Icon
REM ======================================================

echo Building Synthwave Gift Catalog...

REM Define Paths
set SRC_DIR=src
set MAIN_FILE=app.py
set ICON_PATH=assets/icons/favicon.ico
set DIST_NAME=Gift Catalog.exe

REM Clean Previous Builds
rmdir /s /q build
rmdir /s /q dist
del "%SRC_DIR%\%MAIN_FILE:.py=.spec%" 2>nul

REM Build with PyInstaller
pyinstaller --noconfirm --onefile --windowed ^
 --name "Gift Catalog" ^
 --icon "%ICON_PATH%" ^
 "%SRC_DIR%\%MAIN_FILE%"

echo Build Completed.

REM Rename the .exe if Needed
IF NOT EXIST "dist" (
    echo Build Failed. Please Check for Errors.
    pause
    exit /b 1
)

cd dist
IF EXIST "Gift Catalog.exe" (
    echo Executable Named Correctly.
) ELSE (
    ren "app.exe" "Gift Catalog.exe"
)

echo Done. The Executable is Located in the 'dist' Folder.
pause