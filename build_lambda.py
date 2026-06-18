"""
Build script to prepare Lambda deployment package.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def build_lambda_package():
    """Build Lambda deployment package"""
    print("Building Lambda deployment package...")
    
    # Create build directory
    build_dir = Path("build")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()
    
    # Install dependencies
    print("Installing dependencies...")
    deps_dir = build_dir / "python"
    deps_dir.mkdir()
    
    subprocess.run([
        sys.executable, "-m", "pip",
        "install", "-r", "requirements.txt",
        "-t", str(deps_dir),
        "--no-cache-dir"
    ], check=True)
    
    # Copy source code
    print("Copying application code...")
    shutil.copytree("src", build_dir / "src")
    shutil.copy("main.py", build_dir)
    shutil.copy(".env.example", build_dir / ".env")
    
    # Create zip archive
    print("Creating deployment package...")
    archive_name = "lambda-function"
    shutil.make_archive(archive_name, "zip", build_dir)
    
    print(f"Deployment package created: {archive_name}.zip")
    print("\nNext steps:")
    print("1. Upload lambda-function.zip to S3:")
    print("   aws s3 cp lambda-function.zip s3://YOUR_BUCKET_NAME/")
    print("2. Deploy CloudFormation stack:")
    print("   aws cloudformation deploy --template-file aws/cloudformation-template.yaml \\")
    print("     --stack-name rag-stack \\")
    print("     --parameter-overrides S3BucketName=YOUR_BUCKET_NAME \\")
    print("     --capabilities CAPABILITY_IAM")


if __name__ == "__main__":
    build_lambda_package()
