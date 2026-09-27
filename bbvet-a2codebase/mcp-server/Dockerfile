FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY bbvet_mcp_server.py .

ENV MCP_TRANSPORT=http

EXPOSE 8000

CMD ["python", "bbvet_mcp_server.py"]