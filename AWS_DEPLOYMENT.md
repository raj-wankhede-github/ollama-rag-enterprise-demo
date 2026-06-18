# AWS Deployment Guide

This guide provides step-by-step instructions for deploying the Ollama RAG application to AWS Lambda with API Gateway and S3 storage.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Client Application                   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│             AWS API Gateway                              │
│        (REST API Endpoint)                               │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│             AWS Lambda Function                          │
│        (Serverless Compute)                              │
│        - Query Processing                                │
│        - Document Ingestion                              │
│        - RAG Pipeline Execution                          │
└──┬─────────┬──────────────┬───────────────────────────────┘
   │         │              │
   │    ┌────▼───┐     ┌────▼─────┐     ┌──────────┐
   │    │   S3   │     │ DynamoDB  │     │ Chroma   │
   │    │ Bucket │     │  Table    │     │ Database │
   │    └────────┘     └───────────┘     └──────────┘
   │  Document Storage  Metadata Store  Embeddings
```

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed and configured
- Python 3.9+ installed locally
- Docker (optional, for testing)

## Step-by-Step Deployment

### 1. Create S3 Bucket

```bash
# Create bucket
BUCKET_NAME="my-rag-documents-$(date +%s)"
aws s3 mb s3://${BUCKET_NAME} --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket ${BUCKET_NAME} \
  --versioning-configuration Status=Enabled
```

### 2. Build Lambda Deployment Package

```bash
# Build the deployment package
python build_lambda.py

# This creates: lambda-function.zip with all dependencies
```

### 3. Upload to S3

```bash
# Upload the Lambda package
aws s3 cp lambda-function.zip s3://${BUCKET_NAME}/

# Upload layer (if using dependencies layer)
aws s3 cp build/python.zip s3://${BUCKET_NAME}/lambda-layer.zip
```

### 4. Deploy CloudFormation Stack

```bash
# Deploy the stack
aws cloudformation deploy \
  --template-file aws/cloudformation-template.yaml \
  --stack-name ollama-rag-stack \
  --parameter-overrides \
    S3BucketName=${BUCKET_NAME} \
    LambdaTimeout=600 \
    LambdaMemory=1024 \
  --capabilities CAPABILITY_IAM \
  --region us-east-1
```

### 5. Get the API Endpoint

```bash
# Retrieve the API Gateway endpoint
API_ENDPOINT=$(aws cloudformation describe-stacks \
  --stack-name ollama-rag-stack \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' \
  --output text \
  --region us-east-1)

echo "API Endpoint: ${API_ENDPOINT}"
```

## Testing the Deployment

### 1. Test Health Endpoint

```bash
curl ${API_ENDPOINT}/health

# Response should include:
# {
#   "status": "healthy",
#   "environment": "aws",
#   "ollama_available": false/true
# }
```

### 2. Ingest a Document

```bash
# Create a test file
echo "Artificial Intelligence is transforming technology" > test.txt

# Upload via Lambda
curl -X POST ${API_ENDPOINT}/ingest \
  -F "file=@test.txt"
```

### 3. Query the System

```bash
curl -X POST ${API_ENDPOINT}/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is AI?",
    "top_k": 5
  }'
```

## Configuration for AWS

### Environment Variables in Lambda

The CloudFormation template automatically sets:

```yaml
ENV: aws
STORAGE_TYPE: s3
AWS_S3_BUCKET: your-bucket-name
VECTOR_DB_TYPE: chroma
LOG_LEVEL: INFO
```

### Modify Lambda Configuration

```bash
# Update environment variables
aws lambda update-function-configuration \
  --function-name ollama-rag-function \
  --environment Variables='{
    "ENV=aws",
    "LOG_LEVEL=DEBUG"
  }' \
  --region us-east-1
```

## Monitoring and Troubleshooting

### 1. View Lambda Logs

```bash
# Get recent logs
aws logs tail /aws/lambda/ollama-rag-function --follow

# Get specific log stream
aws logs get-log-events \
  --log-group-name /aws/lambda/ollama-rag-function \
  --log-stream-name 'YYYY/MM/DD/[$LATEST]hash'
```

### 2. Monitor CloudWatch Metrics

```bash
# Get invocation metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=ollama-rag-function \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

### 3. Check S3 Storage

```bash
# List uploaded documents
aws s3 ls s3://${BUCKET_NAME}/documents/

# Download a file for inspection
aws s3 cp s3://${BUCKET_NAME}/documents/filename.txt ./
```

## Scaling Considerations

### 1. Lambda Concurrency

```bash
# Set reserved concurrency
aws lambda put-function-concurrency \
  --function-name ollama-rag-function \
  --reserved-concurrent-executions 10
```

### 2. S3 Optimization

- Enable S3 Transfer Acceleration for faster uploads
- Use S3 Intelligent-Tiering for cost optimization
- Configure CORS if needed for web clients

### 3. DynamoDB Scaling

```bash
# Set on-demand billing (for variable load)
aws dynamodb update-table \
  --table-name rag-embeddings \
  --billing-mode PAY_PER_REQUEST
```

## Cost Estimation

Typical usage patterns (1000 requests/month):

- **Lambda**: ~$0.20/month
  - 1GB memory × 5 second average = 5GB-seconds per request
  - 1000 requests × 5GB-sec = 5000 GB-sec
  - Price: $0.0000166667/GB-sec

- **S3**: ~$0.50/month (for storage)
  - 1GB storage = $0.023
  - Plus API calls: ~$0.0004

- **DynamoDB**: ~$0.30/month (on-demand)
  - Read capacity: 100 WRU per request average
  - Write capacity: minimal

- **API Gateway**: ~$3.50/month
  - 1000 requests × 3.5 per million

**Total: ~$4-5 per month for typical usage**

## Cleanup

### Remove CloudFormation Stack

```bash
# Delete the stack (this will remove Lambda, API Gateway, IAM roles, etc.)
aws cloudformation delete-stack \
  --stack-name ollama-rag-stack \
  --region us-east-1

# Monitor deletion
aws cloudformation wait stack-delete-complete \
  --stack-name ollama-rag-stack \
  --region us-east-1
```

### Remove S3 Bucket

```bash
# Empty the bucket first
aws s3 rm s3://${BUCKET_NAME} --recursive

# Delete the bucket
aws s3 rb s3://${BUCKET_NAME}
```

## Advanced Configuration

### Custom Domain Name

```bash
# Create certificate in ACM
# Then create custom domain mapping in API Gateway
aws apigateway create-domain-name \
  --domain-name api.example.com \
  --certificate-arn arn:aws:acm:region:account:certificate/id
```

### Enable API Key Authentication

```bash
# Create API key
aws apigateway create-api-key \
  --name "RAG-API-Key" \
  --enabled

# Create usage plan
aws apigateway create-usage-plan \
  --name "RAG-Usage-Plan" \
  --api-stages apiId=${API_ID},stage=prod
```

### Enable WAF Protection

```bash
# Create WAF for API Gateway
aws wafv2 create-web-acl \
  --name RAG-WAF \
  --scope REGIONAL \
  --default-action Block={} \
  --rules file://waf-rules.json
```

## Support

For issues during deployment:

1. Check CloudWatch logs: `aws logs tail /aws/lambda/ollama-rag-function`
2. Verify IAM permissions
3. Check S3 bucket policies
4. Review CloudFormation stack events
5. Test locally first with Docker

---

**Deployment completed! Your RAG system is now running on AWS Lambda.**
