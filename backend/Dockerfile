FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure Python output is sent directly to the terminal
ENV PYTHONUNBUFFERED=1

# Install the uv package manager
RUN pip install --no-cache-dir uv
# Copy dependency definition files first.
# This allows Docker to cache dependency installation.
COPY pyproject.toml uv.lock ./

# Install project dependencies from the lock file
RUN uv sync --frozen


# --------------------------------------------------------------------
# Classic pip workflow (reference only)
#
# Uncomment the following lines if I decide to use pip instead of uv.
#
# COPY pyproject.toml ./
# RUN pip install --no-cache-dir .
# --------------------------------------------------------------------

# Copy the application source code
COPY . .
# Copy entrypoint.sh
COPY scripts/entrypoint.sh /entrypoint.sh
# Create a non-root user for improved container security
RUN useradd --create-home app
# Allow permission for app user
RUN chown -R app:app /app
# Allow permission for entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch to the non-root user
USER app

# Expose the application port
EXPOSE 8000

# Entrypoint handles the pre-start migration work
ENTRYPOINT ["/entrypoint.sh"]

# Start the FastAPI application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Classic pip command
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
