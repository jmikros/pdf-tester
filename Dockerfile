# =============================================
# PDF-Tester CLI - Docker Image (CLI only)
# =============================================

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies needed for PDF libraries (pymupdf, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpoppler-cpp-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install the package
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -e .

# Create non-root user for better security
RUN useradd -m -u 1000 tester && chown -R tester:tester /app
USER tester

# Volume for mounting your PDFs from host machine
VOLUME ["/data"]

# Make sure the CLI is in PATH
ENV PATH="/home/tester/.local/bin:${PATH}"

ENTRYPOINT ["pdf-tester"]
CMD ["--help"]