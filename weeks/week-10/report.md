## Docker build report

The image is built using multi-stage Docker build.

## Layers explanation

### Stage 1 (builder)
- base image: python:3.11-slim
- installs dependencies via pip
- creates dependency layer

Each command creates a new layer:
1. FROM python:3.11-slim
2. COPY requirements.txt
3. RUN pip install

### Stage 2 (runtime)
- base image: python:3.11-slim
- copies installed packages from builder stage
- copies application source code

Each command creates a new layer:
1. FROM python:3.11-slim
2. COPY from builder (/install -> /usr/local)
3. COPY source code

## Image size

Final Docker image size: ~70-100 MB (depends on system build)
