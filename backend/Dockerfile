# =============================================================================
# TransformIQ Backend — Dockerfile
# =============================================================================
FROM python:3.11-slim

# Install system dependencies required by document processing libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && python -m spacy download en_core_web_sm

# Optional build arg to bake the Hugging Face BERT NER weights into the image
# for air-gapped deployments: docker build --build-arg PRELOAD_BERT_PII=true
ARG PRELOAD_BERT_PII=false
RUN if [ "$PRELOAD_BERT_PII" = "true" ]; then \
        python -c "from transformers import AutoTokenizer, AutoModelForTokenClassification; AutoTokenizer.from_pretrained('dslim/bert-base-NER'); AutoModelForTokenClassification.from_pretrained('dslim/bert-base-NER')"; \
    fi

# Copy application source
COPY . .

# Create storage directory for local filesystem adapter
RUN mkdir -p /app/storage

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=15s --timeout=10s --start-period=20s --retries=5 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
