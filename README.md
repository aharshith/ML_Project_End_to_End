#End to End Machine Learning Project

**Project Deployment to AWS using EC2 + ECR + GitHub Actions**

1. Dockerize Your Application
Create a Dockerfile:

dockerfile
Copy
Edit
FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
Build Docker Image:

bash
Copy
Edit
docker build -t student-performance-app .

**2. Push Docker Image to AWS ECR****
Step 1: Create an IAM user
Go to AWS Console → IAM → Users → Create user.

Give programmatic access.

Attach these policies:

AmazonEC2FullAccess

AmazonEC2ContainerRegistryFullAccess

Download the CSV file with access and secret keys.

Step 2: Create an ECR repository
Go to AWS Console → ECR → Create Repository.

Name: student-performance

Visibility: Private

Note down the Repository URI.

3. Setup GitHub Secrets
In your GitHub repo:

Go to Settings → Secrets → Actions.

Add the following secrets:
| Secret Name | Value |
|-------------|-------|
| AWS_ACCESS_KEY_ID | From IAM CSV |
| AWS_SECRET_ACCESS_KEY | From IAM CSV |
| AWS_REGION | e.g., us-east-1 |
| ECR_REPOSITORY | student-performance |
| ECR_REGISTRY | e.g., 123456789012.dkr.ecr.us-east-1.amazonaws.com |

4. Create GitHub Actions Workflow
Create .github/workflows/deploy.yaml in your repo:


    
5. Create an EC2 Instance (Ubuntu)
Go to EC2 → Launch Instance

Choose:

OS: Ubuntu 22.04 LTS

Instance type: t2.micro (Free tier)

Port 80 & 5000 open in Security Groups

Download the .pem key

6. Setup EC2 (Runner)
SSH into EC2:

bash
Copy
Edit
ssh -i key.pem ubuntu@<ec2-public-ip>
Install Docker:

bash
Copy
Edit
sudo apt update && sudo apt install docker.io -y
sudo usermod -aG docker ubuntu
Install GitHub Runner:

bash
Copy
Edit
# Go to your GitHub → Settings → Actions → Runners → Add runner
# Follow instructions to install and configure runner
Start the runner:

bash
Copy
Edit
./run.sh
7. Trigger Deployment
Push a change to your GitHub main branch.

GitHub Actions will:

Build Docker image

Push it to ECR

Run it on EC2 via self-hosted runner

✅ Final Verification
Open browser and navigate to http://<EC2-Public-IP>

App should be live and predictions working.

🧹 Optional Cleanup (To Avoid Charges)
Stop/terminate EC2 instance

Delete ECR repository

Remove GitHub secrets and runners

If you'd like to deploy this on Azure (instead of AWS), I can provide an equivalent step-by-step process using Azure App Service or Azure Container Instances.
