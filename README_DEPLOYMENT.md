# 🚀 AWS Deployment Guide — Hospital Insurance Claims Analytics

Complete step-by-step deployment to **AWS EC2 + ECR** using Docker.

**Architecture:**
```
Local (VS Code)  →  GitHub  →  ECR (image)  →  EC2 (container)  →  Public URL
```

**Estimated time:** 45–60 minutes (first time)
**Cost:** Free tier eligible (~$0 for 12 months, then ~$8/month)

---

## 📋 Prerequisites Checklist

Before starting, verify you have:

| # | Requirement | Check Command |
|---|-------------|---------------|
| 1 | AWS account | https://aws.amazon.com |
| 2 | IAM user with EC2 + ECR access | AWS Console → IAM |
| 3 | AWS CLI installed locally | `aws --version` |
| 4 | AWS CLI configured | `aws configure list` |
| 5 | Docker Desktop installed | `docker --version` |
| 6 | Git installed | `git --version` |
| 7 | Project pushed to GitHub | `git remote -v` |
| 8 | `.env` file present locally | `type .env` |

**If any tool is missing → stop and install it first.**

---

## 🎯 Deployment Phases

| Phase | Where | Time |
|-------|-------|------|
| Phase 1 | Local (VS Code) | 5 min |
| Phase 2 | Local (VS Code) | 5 min |
| Phase 3 | Local (VS Code) | 3 min |
| Phase 4 | Local (VS Code) | 3 min |
| Phase 5 | Local (VS Code) | 5 min |
| Phase 6 | AWS Console | 10 min |
| Phase 7 | EC2 Terminal (SSH) | 5 min |
| Phase 8 | EC2 Terminal (SSH) | 3 min |
| Phase 9 | EC2 Terminal (SSH) | 3 min |
| Phase 10 | Local (VS Code) | 2 min |
| Phase 11 | (Optional) EC2 | 10 min |

---

## 🖥️ PHASE 1 — Local: Prepare Files

**Terminal:** VS Code terminal (project root)

### 1.1 Create `Dockerfile`

**File:** `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# System dependencies for pyodbc
RUN apt-get update && apt-get install -y \
    gcc g++ unixodbc-dev curl gnupg2 apt-transport-https \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY 03_Python_Analysis/ ./03_Python_Analysis/
COPY 04_Streamlit/       ./04_Streamlit/
COPY data/               ./data/
COPY 06_Logs/            ./06_Logs/

EXPOSE 8501

CMD ["streamlit", "run", "04_Streamlit/app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
```

### 1.2 Create `.dockerignore`

**File:** `.dockerignore`

```
env/
venv/
.venv/
.git/
.gitignore
.env
__pycache__/
*.pyc
.ipynb_checkpoints/
05_Testing/
01_Business_Analysis/
02_Database/
06_Logs/*.log
*.zip
.DS_Store
```

### 1.3 Verify data is committed

```bash
git add -f data/claims_main.csv
git add -f data/data_dictionary.csv
git add -f data/denial_labels.csv
git status
```

---

## 🖥️ PHASE 2 — Local: Test Docker Build

**Terminal:** VS Code terminal

### 2.1 Build the image

```bash
docker build -t hospital-claims-analytics:latest .
```

**Expected:** `Successfully tagged hospital-claims-analytics:latest`

### 2.2 Run the container locally

```bash
docker run -d -p 8501:8501 --name claims-test hospital-claims-analytics:latest
```

### 2.3 Verify

```bash
docker ps
```

**Expected:** Container `claims-test` running on `0.0.0.0:8501->8501/tcp`

Open browser:
```
http://localhost:8501
```

✅ Dashboard works? → Continue.
❌ Doesn't work? → Check `docker logs claims-test` and fix before deploying.

### 2.4 Stop and clean up

```bash
docker stop claims-test
docker rm claims-test
```

---

## 🖥️ PHASE 3 — Local: Configure AWS CLI

**Terminal:** VS Code terminal

### 3.1 Verify AWS CLI is configured

```bash
aws configure list
```

**Expected output:**
```
      Name                    Value             Type    Location
      ----                    -----             ----    --------
   profile                <not set>             None    None
access_key     ****************XXXX              env
secret_key     ****************YYYY              env
    region                us-east-1              env
```

### 3.2 If not configured

```bash
aws configure
```

Enter:
- **AWS Access Key ID:** (from IAM user)
- **AWS Secret Access Key:** (from IAM user)
- **Default region:** `us-east-1` (or your preferred region)
- **Output format:** `json`

### 3.3 Verify identity

```bash
aws sts get-caller-identity
```

**Expected:** JSON with your `Account`, `UserId`, `Arn`

### 3.4 Set shell variables (for this session)

**Windows PowerShell:**
```powershell
$ACCOUNT_ID = "123456789012"  # ← your account ID
$REGION     = "us-east-1"     # ← your region
$REPO       = "hospital-claims-analytics"
```

**macOS / Linux / Git Bash:**
```bash
export ACCOUNT_ID="123456789012"
export REGION="us-east-1"
export REPO="hospital-claims-analytics"
```

To find your `ACCOUNT_ID`:
```bash
aws sts get-caller-identity --query Account --output text
```

---

## 🖥️ PHASE 4 — Local: Create ECR Repository

**Terminal:** VS Code terminal

### 4.1 Check if repository exists

```bash
aws ecr describe-repositories --region us-east-1
```

If `hospital-claims-analytics` is listed → skip to Phase 5.

### 4.2 Create repository

```bash
aws ecr create-repository \
    --repository-name hospital-claims-analytics \
    --region us-east-1
```

**Expected output:**
```json
{
    "repository": {
        "repositoryUri": "123456789012.dkr.ecr.us-east-1.amazonaws.com/hospital-claims-analytics",
        ...
    }
}
```

**Copy the `repositoryUri`** — you'll use it in Phase 5.

---

## 🖥️ PHASE 5 — Local: Push Image to ECR

**Terminal:** VS Code terminal

### 5.1 Login to ECR

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
```

**Expected:** `Login Succeeded`

### 5.2 Tag image

```bash
docker tag hospital-claims-analytics:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/hospital-claims-analytics:latest
```

### 5.3 Push image

```bash
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/hospital-claims-analytics:latest
```

**Expected:**
```
The push refers to repository [123456789012.dkr.ecr.us-east-1.amazonaws.com/hospital-claims-analytics]
...
latest: digest: sha256:... size: ...
```

### 5.4 Verify in ECR

```bash
aws ecr list-images --repository-name hospital-claims-analytics --region us-east-1
```

**Expected:** JSON showing `imageTag: latest`

---

## ☁️ PHASE 6 — AWS Console: Launch EC2

**Location:** AWS Console (browser) — not terminal

### 6.1 Go to EC2

1. Open https://console.aws.amazon.com/ec2
2. Change region (top right) to **us-east-1** (or your region)
3. Click **Launch Instance**

### 6.2 Configure instance

| Setting | Value |
|---------|-------|
| **Name** | `hospital-claims-server` |
| **AMI** | Ubuntu Server 22.04 LTS |
| **Instance type** | `t3.micro` (free tier) or `t3.small` |
| **Key pair** | Create new → `claims-key.pem` → download |
| **Network** | Default VPC |

### 6.3 Security Group Rules

Click **Edit** next to Network settings → **Add rule** for each:

| Type | Port | Source | Purpose |
|------|------|--------|---------|
| SSH | 22 | My IP | SSH access |
| HTTP | 80 | 0.0.0.0/0 | Public access |
| Custom TCP | 8501 | 0.0.0.0/0 | (optional, backup) |

### 6.4 Storage

- **Size:** 20 GB
- **Type:** gp3

### 6.5 Advanced — IAM Instance Profile

Under **Advanced details**:

1. **IAM instance profile:** `EC2-ECR-ReadRole`
2. If not listed, first create it in IAM Console:
   - IAM → Roles → Create role → AWS service → EC2
   - Attach policy: `AmazonEC2ContainerRegistryReadOnly`
   - Name: `EC2-ECR-ReadRole`

### 6.6 Launch

Click **Launch Instance**.

Wait ~60 seconds → Instance state = **Running**.

**Copy the Public IPv4 address** — you'll need it in Phase 7.

---

## 🐧 PHASE 7 — EC2 Terminal: Install Docker

**Terminal:** Local VS Code terminal (SSH into EC2)

### 7.1 Move key file (Windows)

```bash
# Move downloaded .pem file to your project or user folder
move %USERPROFILE%\Downloads\claims-key.pem %USERPROFILE%\.ssh\
```

### 7.2 SSH into EC2

Replace `<EC2_PUBLIC_IP>` with the IP from Phase 6.

```bash
ssh -i %USERPROFILE%\.ssh\claims-key.pem ubuntu@<EC2_PUBLIC_IP>
```

**First-time prompt:** type `yes` when asked to trust the host.

**Expected prompt:**
```
ubuntu@ip-172-31-XX-XX:~$
```

### 7.3 Update OS

```bash
sudo apt update && sudo apt upgrade -y
```

### 7.4 Install Docker + AWS CLI

```bash
sudo apt install -y docker.io awscli
```

### 7.5 Enable Docker on boot

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

### 7.6 Allow ubuntu user to use Docker

```bash
sudo usermod -aG docker ubuntu
```

### 7.7 Reconnect for group change to apply

```bash
exit
```

Then SSH again:

```bash
ssh -i %USERPROFILE%\.ssh\claims-key.pem ubuntu@<EC2_PUBLIC_IP>
```

### 7.8 Verify

```bash
docker --version
aws --version
```

**Expected:**
```
Docker version 24.x.x
aws-cli/2.x.x
```

---

## 🐧 PHASE 8 — EC2 Terminal: Pull Image from ECR

**Terminal:** EC2 SSH session

### 8.1 Verify IAM role works

```bash
aws sts get-caller-identity
```

**Expected:** JSON with `Arn` containing `EC2-ECR-ReadRole`.

### 8.2 Login to ECR (uses IAM role — no credentials needed)

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
```

**Expected:** `Login Succeeded`

### 8.3 Pull the image

```bash
docker pull 123456789012.dkr.ecr.us-east-1.amazonaws.com/hospital-claims-analytics:latest
```

**Expected:** Layers download, image appears.

### 8.4 Verify

```bash
docker images
```

**Expected:** Your image listed.

---

## 🐧 PHASE 9 — EC2 Terminal: Run Container

**Terminal:** EC2 SSH session

### 9.1 Run the container

```bash
docker run -d \
    --name claims-app \
    --restart unless-stopped \
    -p 80:8501 \
    -e CSV_PATH=data/claims_main.csv \
    -e PROCESSING_THRESHOLD_DAYS=30 \
    -e DB_TRUSTED_CONNECTION=no \
    123456789012.dkr.ecr.us-east-1.amazonaws.com/hospital-claims-analytics:latest
```

**What each flag does:**
| Flag | Purpose |
|------|---------|
| `-d` | Run in background |
| `--name claims-app` | Container name |
| `--restart unless-stopped` | Auto-restart after reboot |
| `-p 80:8501` | Expose Streamlit on port 80 |
| `-e ...` | Environment variables |

### 9.2 Verify container is running

```bash
docker ps
```

**Expected:**
```
CONTAINER ID   IMAGE                                              STATUS         PORTS
abc123def456   .../hospital-claims-analytics:latest              Up 10 seconds  0.0.0.0:80->8501/tcp
```

### 9.3 Check logs

```bash
docker logs -f claims-app
```

**Expected:** Streamlit startup messages.
Press **Ctrl + C** to exit log view (container keeps running).

### 9.4 Test from EC2

```bash
curl http://localhost:80
```

**Expected:** HTML output (Streamlit page).

---

## 🖥️ PHASE 10 — Local: Test Public Access

**Terminal:** Any browser

Open:
```
http://<EC2_PUBLIC_IP>
```

**Example:** `http://54.201.123.45`

### If it works

✅ **Deployment complete!** Bookmark the URL.

### If it doesn't work

| Symptom | Cause | Fix |
|---------|-------|-----|
| Connection timeout | Security group missing port 80 | Add HTTP rule in EC2 → Security |
| Blank page | Container crashed | `docker logs claims-app` on EC2 |
| 502 Bad Gateway | Wrong port mapping | Check `-p 80:8501` in run command |
| ERR_CONNECTION_REFUSED | EC2 firewall | `sudo ufw status` → `sudo ufw allow 80` |

---

## ⚙️ PHASE 11 — (Optional) Nginx + HTTPS

**Terminal:** EC2 SSH session

Only if you have a domain pointing to your EC2 IP.

### 11.1 Install Nginx + Certbot

```bash
sudo apt install -y nginx certbot python3-certbot-nginx
```

### 11.2 Configure reverse proxy

```bash
sudo nano /etc/nginx/sites-available/claims
```

Paste:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 86400;
    }
}
```

Save: **Ctrl + O → Enter → Ctrl + X**

### 11.3 Enable site

```bash
sudo ln -s /etc/nginx/sites-available/claims /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 11.4 Get SSL certificate

```bash
sudo certbot --nginx -d your-domain.com
```

Follow prompts → HTTPS enabled.

### 11.5 Verify

Open: `https://your-domain.com`

---

## 🔄 Update Workflow (After First Deploy)

Every time you change code:

### Terminal 1 — Local (VS Code)

```bash
# 1. Commit + push
git add .
git commit -m "Update dashboard"
git push

# 2. Rebuild image
docker build -t hospital-claims-analytics:latest .

# 3. Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# 4. Tag
docker tag hospital-claims-analytics:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/hospital-claims-analytics:latest

# 5. Push
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/hospital-claims-analytics:latest
```

### Terminal 2 — EC2 (SSH)

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Pull new image
docker pull 123456789012.dkr.ecr.us-east-1.amazonaws.com/hospital-claims-analytics:latest

# Restart container
docker stop claims-app
docker rm claims-app

docker run -d \
    --name claims-app \
    --restart unless-stopped \
    -p 80:8501 \
    -e CSV_PATH=data/claims_main.csv \
    -e DB_TRUSTED_CONNECTION=no \
    123456789012.dkr.ecr.us-east-1.amazonaws.com/hospital-claims-analytics:latest
```

### Or use `deploy.sh` (automated)

**File:** `deploy.sh` (project root, local)

```bash
#!/bin/bash
set -e

ACCOUNT_ID=123456789012
REGION=us-east-1
REPO=hospital-claims-analytics
IMAGE=$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO:latest
EC2_HOST=ubuntu@<EC2_PUBLIC_IP>
PEM=~/.ssh/claims-key.pem

echo "🔨 Building..."
docker build -t $REPO:latest .

echo "🏷️  Tagging..."
docker tag $REPO:latest $IMAGE

echo "🔐 ECR login..."
aws ecr get-login-password --region $REGION | \
    docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

echo "⬆️  Pushing..."
docker push $IMAGE

echo "🚀 Deploying on EC2..."
ssh -i $PEM $EC2_HOST "
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

echo "✅ Deployed: http://$EC2_HOST"
```

Run:
```bash
chmod +x deploy.sh
bash deploy.sh
```

---

## 🐞 Troubleshooting

### Local Docker build fails

| Error | Fix |
|-------|-----|
| `Cannot connect to Docker daemon` | Start Docker Desktop |
| `pyodbc install failed` | Add `unixodbc-dev` to Dockerfile (already included) |
| `ModuleNotFoundError` | Check `requirements.txt` has all packages |

### ECR push fails

| Error | Fix |
|-------|-----|
| `denied: Your authorization token has expired` | Re-run `aws ecr get-login-password ...` |
| `no basic auth credentials` | Login to ECR again |
| `repository does not exist` | Create it: `aws ecr create-repository ...` |

### EC2 SSH fails

| Error | Fix |
|-------|-----|
| `Permission denied (publickey)` | Use correct `.pem` file, chmod 400 |
| `Connection timed out` | Security group missing SSH rule |
| `Host key verification failed` | `ssh-keygen -R <EC2_IP>` |

### Container runs but page doesn't load

| Symptom | Fix |
|---------|-----|
| `docker ps` shows container | Check `docker logs claims-app` |
| Container exited | `docker start claims-app` |
| Port not exposed | Verify `-p 80:8501` |
| Security group blocks | Add HTTP rule |

### Streamlit errors in container

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: src` | Check `COPY 03_Python_Analysis/` in Dockerfile |
| `CSV not found` | Check `data/claims_main.csv` committed to git |
| `Permission denied` writing logs | Mount volume or use `/tmp` |

---

## 💰 Cost Estimate

| Service | Free Tier | After |
|---------|-----------|-------|
| EC2 t3.micro | $0 (12 months) | ~$8/month |
| ECR storage | 500 MB free | ~$0.10/GB |
| Data transfer | 100 GB free | ~$0.09/GB |
| **Total** | **~$0** | **~$8–10/month** |

**Tip:** Stop the EC2 instance when not in use to save costs.

---

## 🔐 Security Checklist

| ✅ | Item |
|----|------|
| ☐ | `.env` NOT committed to git |
| ☐ | No credentials in Dockerfile |
| ☐ | IAM user has least privilege |
| ☐ | EC2 instance role = ECR read only |
| ☐ | Security group restricts SSH to your IP |
| ☐ | HTTPS enabled (production) |
| ☐ | No real patient data |
| ☐ | Container runs as non-root (optional) |

---

## 🎯 Final Deployment Checklist

| # | Phase | Task | Done |
|---|-------|------|------|
| 1 | Local | `Dockerfile` created | ⬜ |
| 2 | Local | `.dockerignore` created | ⬜ |
| 3 | Local | CSV data committed | ⬜ |
| 4 | Local | Docker builds successfully | ⬜ |
| 5 | Local | Container runs locally | ⬜ |
| 6 | Local | AWS CLI configured | ⬜ |
| 7 | Local | ECR repository exists | ⬜ |
| 8 | Local | Image pushed to ECR | ⬜ |
| 9 | AWS | EC2 launched | ⬜ |
| 10 | AWS | Security group allows 80/22 | ⬜ |
| 11 | AWS | IAM role attached to EC2 | ⬜ |
| 12 | EC2 | Docker installed | ⬜ |
| 13 | EC2 | Image pulled from ECR | ⬜ |
| 14 | EC2 | Container running | ⬜ |
| 15 | Browser | Public URL works | ⬜ |
| 16 | EC2 | (Optional) Nginx + HTTPS | ⬜ |

---

## 🎉 Success Indicators

After deployment, you should have:

| Item | Expected |
|------|----------|
| Public URL | `http://<EC2_IP>` |
| Dashboard | Loads with KPIs and charts |
| Data source badge | Shows "CSV (DenialIQ)" or "Sample" |
| Docker container | `docker ps` shows `claims-app` running |
| Auto-restart | Enabled via `--restart unless-stopped` |
| HTTPS (optional) | `https://your-domain.com` |

---

## 📞 Support

| Issue | Resource |
|-------|----------|
| Docker errors | https://docs.docker.com |
| ECR errors | AWS Console → ECR → Troubleshooting |
| EC2 errors | AWS Console → EC2 → Instance Logs |
| Streamlit errors | https://docs.streamlit.io |

---

> **Note:** This deployment uses **synthetic data only**. No real patient
> information is stored or transmitted anywhere in the pipeline.