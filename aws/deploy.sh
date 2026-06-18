#!/bin/bash

# Deployment script for AWS Lambda

set -e

echo "Building Lambda deployment package..."

# Create deployment directory
mkdir -p build
cd build

# Install dependencies
pip install -r ../requirements.txt -t python/

# Copy application code
cp -r ../src ./
cp ../main.py ./
cp ../.env.example .env

# Create deployment package
zip -r lambda-function.zip . -x "*.pyc" "*.pyo" "__pycache__/*"

echo "Deployment package created: build/lambda-function.zip"
echo ""
echo "To deploy to AWS Lambda:"
echo "1. Update environment variables in CloudFormation template"
echo "2. Deploy CloudFormation stack"
echo "3. Upload lambda-function.zip to S3"
echo ""
echo "Deploy command:"
echo "aws s3 cp lambda-function.zip s3://YOUR_BUCKET_NAME/"
echo "aws cloudformation deploy --template-file aws/cloudformation-template.yaml --stack-name rag-stack --parameter-overrides S3BucketName=YOUR_BUCKET_NAME --capabilities CAPABILITY_IAM"
