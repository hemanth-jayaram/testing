@echo off
echo ========================================
echo Federated Learning Project Cleanup
echo ========================================
echo.

echo This script will remove unnecessary and duplicate files.
echo.
echo Files to be removed:
echo   - devops-key.pem (SECURITY RISK - Private Key)
echo   - DEPLOY_INSTRUCTIONS.md (duplicate)
echo   - DEPLOYMENT.md (duplicate)
echo   - run_local.py (redundant)
echo.

set /p confirm="Do you want to proceed? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo Cleanup cancelled.
    exit /b
)

echo.
echo Starting cleanup...
echo.

REM Remove private key (CRITICAL)
if exist devops-key.pem (
    echo [1/4] Removing devops-key.pem...
    del /F /Q devops-key.pem 2>nul
    if exist devops-key.pem (
        echo   WARNING: Could not delete devops-key.pem - Please delete manually!
        echo   This is a SECURITY RISK!
    ) else (
        echo   SUCCESS: devops-key.pem removed
    )
) else (
    echo [1/4] devops-key.pem already removed
)

REM Remove duplicate documentation
if exist DEPLOY_INSTRUCTIONS.md (
    echo [2/4] Removing DEPLOY_INSTRUCTIONS.md...
    del /F /Q DEPLOY_INSTRUCTIONS.md
    echo   SUCCESS: DEPLOY_INSTRUCTIONS.md removed
) else (
    echo [2/4] DEPLOY_INSTRUCTIONS.md already removed
)

if exist DEPLOYMENT.md (
    echo [3/4] Removing DEPLOYMENT.md...
    del /F /Q DEPLOYMENT.md
    echo   SUCCESS: DEPLOYMENT.md removed
) else (
    echo [3/4] DEPLOYMENT.md already removed
)

REM Remove redundant script
if exist run_local.py (
    echo [4/4] Removing run_local.py...
    del /F /Q run_local.py
    echo   SUCCESS: run_local.py removed
) else (
    echo [4/4] run_local.py already removed
)

echo.
echo ========================================
echo Cleanup Complete!
echo ========================================
echo.
echo New files added:
echo   + .gitignore (prevents future security issues)
echo   + model_stats.py (fixes missing import)
echo   + DEPLOYMENT_GUIDE.md (consolidated documentation)
echo.
echo Next steps:
echo   1. Review CLEANUP_SUMMARY.md for details
echo   2. Test the application: python app.py
echo   3. If using Git, commit changes
echo.
pause
