# Use the official Python image from the Docker Hub
FROM python:3.11

# Install Java
RUN apt-get update && apt-get install -y openjdk-11-jre-headless

# Set JAVA_HOME environment variable
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ENV PATH $JAVA_HOME/bin:$PATH

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# Run the application
CMD ["python3", "main.py"]