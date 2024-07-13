FROM python:3

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Set working directory
WORKDIR /usr/src/app

# Copy requirements.txt first
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
