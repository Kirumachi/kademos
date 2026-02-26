FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install .[cli]

COPY tools/ ./tools/
COPY 01-ASVS-Core-Reference/ ./01-ASVS-Core-Reference/
COPY 00-Documentation-Standards/ ./00-Documentation-Standards/

ENTRYPOINT ["kademos"]
CMD ["--help"]
