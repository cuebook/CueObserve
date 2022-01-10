aws ecr get-login-password --region $aws_region | docker login --username AWS --password-stdin $aws_account_id.dkr.ecr.$aws_region.amazonaws.com

aws ecr create-repository \
    --repository-name cueobserve-lambda-image \
    --image-scanning-configuration scanOnPush=true \
    --region $aws_region

cd api/ops/tasks/detection

docker build -t cueobserve-lambda-image .

docker tag cueobserve-lambda-image:latest $aws_account_id.dkr.ecr.$aws_region.amazonaws.com/cueobserve-lambda-image:latest

docker push $aws_account_id.dkr.ecr.$aws_region.amazonaws.com/cueobserve-lambda-image:latest