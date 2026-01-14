# Build stage
FROM python:3.12.2-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc

COPY requirements.txt .

# Build the wheel binaries recursively and install them in the /app/wheels specified by --wheel-dir
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt



# Final stage (do not use alpine.. too much headache)
FROM python:3.12.2-slim

WORKDIR /app

# copy the built wheels from the build stage to /wheels
COPY --from=builder /app/wheels /wheels

RUN pip install --no-cache-dir /wheels/*

COPY . .

ENTRYPOINT [ "python", "/app/flask_website.py" ]