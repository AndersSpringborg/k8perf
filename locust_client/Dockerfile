FROM locustio/locust
COPY locustfile.py .
ENTRYPOINT [ "python", "-m", "locust", "-f", "locustfile.py", "-u", "10", "-r", "10", "--headless", "-t", "2m", "--host", "http://172.31.33.178:80", "--print-stats", "--csv", "exp" ]