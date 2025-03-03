FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

RUN pip install --no-cache-dir psycopg2-binary pandas sqlalchemy

# Copy the rest of the application files
COPY . .

# Run the Python script on container startup
CMD ["python", "populate_db.py"]