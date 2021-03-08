### System requirements   
Linux Ubuntu (bionic)
Python 3.8 +

### Usage   
Run your parser in command-line
```console
youruser:~path/to/project$ python main.py mysite.site
```

Run in Docker:
```console
docker build -t webcrawler .
docker run --mount "type=bind,source=$(pwd),target=/opt/app" --restart=unless-stopped -e PYTHONUNBUFFERED=1 -it webcrawler:latest /bin/bash
python main.py mysite.site
```
docker run option --mount "type=bind,source=$(pwd),target=/opt/app" - use   
for auto update of code in your host to code in running container   
