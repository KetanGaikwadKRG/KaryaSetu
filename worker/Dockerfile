# =============================================================================
# TransformIQ Worker — Dockerfile
# =============================================================================
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY worker/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && python -m spacy download en_core_web_sm

ARG PRELOAD_BERT_PII=false
RUN if [ "$PRELOAD_BERT_PII" = "true" ]; then \
        python -c "from transformers import AutoTokenizer, AutoModelForTokenClassification; AutoTokenizer.from_pretrained('dslim/bert-base-NER'); AutoModelForTokenClassification.from_pretrained('dslim/bert-base-NER')"; \
    fi

COPY worker/*.py /app/
COPY backend/app /backend/app

# The worker imports the shared application package (`app.core.config` etc.)
# which lives at /backend/app. Bake the path into the image so the worker runs
# with the same PYTHONPATH regardless of what an orchestrator injects.
ENV PYTHONPATH=/backend:/app

# Create storage directory (shared volume with backend)
RUN mkdir -p /app/storage

# Worker does not expose HTTP ports.
# Health is monitored via RQ's built-in worker heartbeat.

CMD ["python", "worker.py"]
