set -xe

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=eu-central-1

docker build -f getQuery.Dockerfile -t jisho-api-get-query .
docker tag jisho-api-get-query $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/jisho-api-get-query
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/jisho-api-get-query
