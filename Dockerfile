FROM ubuntu:latest

WORKDIR /app

COPY requirements.txt .
COPY script.sh .

RUN echo '#!/bin/sh\n"$@"' > /usr/bin/sudo && chmod +x /usr/bin/sudo

RUN chmod +x script.sh && bash script.sh

COPY cof.py .

CMD ["/bin/bash", "-c", "source env/bin/activate && python3 cof.py"]

