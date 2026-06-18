@echo off
REM Deployment script for AWS Lambda on Windows

setlocal enabledelayedexpansion

echo Building Lambda deployment package...

REM Create deployment directory
if exist build rmdir /s /q build
mkdir build
cd build

REM Install dependencies
pip install -r ../requirements.txt -t python/

REM Copy application code
robocopy ..\src . /s /e
copy ..\main.py .
copy ..\.env.example .env

REM Create deployment package
if exist lambda-function.zip del lambda-function.zip
for /r . %%F in (*) do (
    if not "%%F"=="lambda-function.zip" (
        REM Archive files using tar (Windows 10+ has tar)
    )
)

echo Deployment package ready in build directory
echo.
echo To deploy to AWS Lambda:
echo 1. Compress build directory to lambda-function.zip
echo 2. Upload to S3
echo 3. Deploy CloudFormation stack
echo.
