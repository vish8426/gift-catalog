@echo off
flutter emulators --launch Medium_Phone_API_36.0
timeout /t 10 /nobreak > NUL
flutter run