#!/bin/bash
set -e

# ============ CONFIGURATION ============
ACCOUNT_ID=123456789012
REGION=us-east-1
REPO=hospital-claims-analytics
IMAGE=$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO:latest
EC2_IP=54.201.123.45
PEM=~/.ssh/claims-key.pem
# =======================================

echo "🔨 Building Docker image..."
docker build -t $REPO:latest .

echo "🏷️  Tagging image..."
docker tag $REPO:latest $IMAGE

echo "🔐 Logging into ECR..."
aws ecr get-login-password --region $REGION | \
    docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

echo "⬆️  Pushing to ECR..."
docker push $IMAGE

echo "🚀 Deploying on EC2..."
ssh -i $PEM ubuntu@$EC2_IP "
    aws ecr get-login-password --region $REGION | \
        docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
    docker pull $IMAGE
    docker stop claims-app || true
    docker rm claims-app || true
    docker run -d --name claims-app --restart unless-stopped \
        -p 80:8501 \
        -e CSV_PATH=data/claims_main.csv \
        -e DB_TRUSTED_CONNECTION=no \
        $IMAGE
"

echo "✅ Deployed successfully!"
echo "🌐 http://$EC2_IP"