# Use an official dbt image
FROM ghcr.io/dbt-labs/dbt-postgres:latest

# Set the working directory
WORKDIR /usr/app

# Copy the dbt project files
COPY ./webshop .

RUN ["ls", "-a"]
# Install dependencies if needed
# RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for dbt profile
ENV DBT_PROFILES_DIR=.

# Run dbt commands (change as needed)
# CMD ["dbt", "run"]