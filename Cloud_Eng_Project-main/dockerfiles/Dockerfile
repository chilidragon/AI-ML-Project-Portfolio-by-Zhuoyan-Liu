FROM python:3.9-slim

# Set the working directory as the current folder
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run when the container starts
CMD ["python", "pipeline.py"]