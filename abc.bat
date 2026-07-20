@echo off
echo Starting automatic GitHub push every 100 seconds...
echo Press Ctrl+C to stop
echo.

:loop
echo [%date% %time%] Starting git operations...
git pull 
git add .
if errorlevel 1 (
    echo Error adding files
    goto wait
)

git commit -m "Auto-commit: %date% %time%"
if errorlevel 1 (
    echo No changes to commit or commit failed
) else (
    echo Commit successful
)

git push
if errorlevel 1 (
    echo Push failed
) else (
    echo Push successful
)

:wait
echo Waiting 100 seconds...
echo.
timeout /t 100 /nobreak

goto loop