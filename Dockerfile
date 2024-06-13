# Use the official Bitnami Spark image
FROM docker.io/bitnami/spark:3.5.0

# Switch to root to install additional packages
USER root

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python packages
RUN python3 -m pip install --upgrade pip

# Set environment variables for Python and Spark integration
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install the required Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# Run the application
CMD ["python3", "main.py"]
