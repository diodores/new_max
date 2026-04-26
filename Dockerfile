FROM python:3.13-alpine
WORKDIR /maxbpt_rebbit
RUN pip install uv
COPY uv.lock pyproject.toml ./
RUN uv sync
COPY . .
ENV PYTHONPATH=/maxbpt_rebbit
CMD ["uv", "run", "uvicorn", "src.main:app"]