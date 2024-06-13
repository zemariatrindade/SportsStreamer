# Sports Content Streaming with Reddit API

![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-E25A1C?style=for-the-badge&logo=Apache%20Spark&logoColor=white)
![git](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white)
![bash](https://img.shields.io/badge/bash-4EAA25?style=for-the-badge&logo=gnu%20bash&logoColor=white)
![markdown](https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white)

This project streams sports content from various subreddits using the Reddit API. It connects to Euro2024, NBA, Tennis, and Copa America subreddits to gather comments and analyze them locally.

## Overview

This application performs the following tasks:
- Connects to the Reddit API to stream sports content from Euro2024, NBA, Tennis, and Copa America subreddits.
- Stores comments locally in the `data/raw` folder.
- Analyzes comments to find references to other users, subreddits, or URLs.
- Computes and prints the top 10 important words based on TF-IDF (Term Frequency-Inverse Document Frequency) analysis.

## Prerequisites

Before running the application, ensure you have Docker and Docker Compose installed on your machine.

1. **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
2. **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Setup

### Step 1: Clone the Repository

Clone the repository to your local machine.

```bash
git clone https://github.com/your-repo/sports-streamer.git
cd sports-streamer
```

### Step 2: Create the `.env` File

Create a .env file in the root directory of the project and add your Reddit API credentials.

```bash
CLIENT_ID=your_client_id
SECRET_TOKEN=your_secret_token
USERNAME=your_reddit_username
PASSWORD=your_reddit_password
```

### Step 3: Build and Run the Docker Container

Build and start the Docker container using Docker Compose.

```bash
Copy code
docker-compose up --build
```

This command will:

- Build the Docker image using the Dockerfile.
- Start the container defined in the docker-compose.yml file.
- Load the environment variables from the .env file.
- Run the application.

### Step 4: Access the Application

Once the container is up and running, you should see logs in the terminal indicating the application is streaming comments from the specified subreddits.

If your application exposes any services or APIs, you can access them through `localhost:8000` or any other port specified in your docker-compose.yml.

## Directory Structure

Ensure your directory structure looks something like this:

```bash
/sports-streamer
|-- data
|-- main.py
|-- producer.py
|-- requirements.txt
|-- Dockerfile
|-- docker-compose.yml
|-- .env
```

## Usage

### Running the Application

To run the application, simply execute the following command:

```bash
docker-compose up --build
```

### Stopping the Application

To stop the application, press CTRL+C in the terminal where Docker Compose is running. To remove the containers, networks, and volumes defined in docker-compose.yml, run:

```bash
docker-compose down
```

### Accessing Logs

To view the logs of the running Docker container, use the following command:

```bash
docker-compose logs -f
```

### Persistent Data

The application stores comments in the data directory, which is mounted as a volume in the Docker container to persist data outside the container's lifecycle.

## Troubleshooting

- Ensure your `.env` file is correctly formatted and contains valid Reddit API credentials.
- Ensure Docker and Docker Compose are installed and running correctly on your machine.
- Check the logs in the terminal for any error messages and troubleshoot accordingly.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. We welcome all contributions.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- [PRAW (Python Reddit API Wrapper)](https://praw.readthedocs.io/en/latest/) for interacting with the Reddit API.
- [NLTK (Natural Language Toolkit)](https://www.nltk.org/) for natural language processing.
- [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) for text analysis.

## Contact

For any questions or issues, please open an issue on the repository or contact the developers.





