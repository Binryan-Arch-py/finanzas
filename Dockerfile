FROM fedora:latest

WORKDIR /app

COPY requirements.txt .
COPY script.sh .

RUN chmod +x script.sh && bash script.sh

COPY cof.py .

CMD ["/bin/bash", "-c", "source env/bin/activate && python3 cof.py"]

