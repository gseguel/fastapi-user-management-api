# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.13-slim AS builder
 
WORKDIR /app
 
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
 
# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.13-slim AS runtime
 
# Non-root user for security
RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser
 
WORKDIR /app
 
# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
 
# Copy application source
COPY app/ ./app/
 
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
 
USER appuser
 
EXPOSE 8080
 
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1