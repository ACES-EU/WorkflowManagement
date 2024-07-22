```shell
docker build -f config/Dockerfile -t pkapsalismartel/set_prefect_scripts .
docker tag pkapsalismartel/set_prefect_scripts:latest pkapsalismartel/set_prefect_scripts:v0.9
docker push pkapsalismartel/set_prefect_scripts:v0.9
```