aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 065885464246.dkr.ecr.us-west-2.amazonaws.com
docker build -t cse291 .
docker tag cse291:latest 065885464246.dkr.ecr.us-west-2.amazonaws.com/cse291:latest
docker push 065885464246.dkr.ecr.us-west-2.amazonaws.com/cse291:latest