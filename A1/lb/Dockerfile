FROM docker:dind
WORKDIR /app
COPY . .

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN apk add --update --no-cache py3-pip

RUN python3 -m pip install --break-system-packages --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["python3", "load_balancer.py"]