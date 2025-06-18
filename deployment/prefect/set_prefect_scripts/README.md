# Build and push image

```bash
TAG=v0.9
IMAGE=ghcr.io/aces-eu/workflowmanagement/set-prefect-scripts:$TAG
PLATFORM=linux/amd64

docker buildx build -f config/Dockerfile --platform $PLATFORM -t $IMAGE .
docker push $IMAGE
```
