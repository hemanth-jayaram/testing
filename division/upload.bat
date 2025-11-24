@echo off
echo ========================================
echo Uploading Division Folder to GitHub
echo Repository: hemanth-jayaram/testing
echo ========================================
echo.

cd /d "%~dp0"

echo Initializing Git repository...
git init

echo Adding remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/hemanth-jayaram/testing.git

echo Staging all files...
git add .

echo Committing files...
git commit -m "Add project division: 4 members + testing suite"

echo Pushing to GitHub...
git branch -M main
git push -u origin main --force

echo.
echo ========================================
echo Upload Complete!
echo ========================================
echo.
echo Visit: https://github.com/hemanth-jayaram/testing
echo.
pause
