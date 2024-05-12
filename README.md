# Dockerized PySpark ETL Pipeline with Delta Tables

This project demonstrates an ETL (Extract, Transform, Load) pipeline using PySpark and Delta Tables, all contained within a Docker environment. It aims to showcase an efficient data processing solution using modern, scalable technologies.

## Requirements

Ensure you have the following dependencies installed:

- **Java 8:** [Installation Guide](https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html)
- **Python 3.6+:** [Download Python](https://www.python.org/downloads/)
- **Docker:** [Get Docker](https://docs.docker.com/get-docker/)
- **PySpark:** [PySpark](https://spark.apache.org/docs/latest/api/python/index.html)
- **Delta Lake:** [Delta Lake](https://delta.io/)

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/temitope777/ho-etl-poc.git
   cd ho-etl-poc
2. **Build the Docker Image:**
   ```bash
   docker build -t ho-etl-app .
3. **Usage:**
   To Run the Application:
   ```bash
   docker run -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output ho-etl-app app
   To run BDD test:
   ```bash
   docker run -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output ho-etl-app test
4. **Configuration:**
   Data and Output Paths: You can adjust the paths for data and output by modifying the mounted volumes in the Docker run commands.
   Spark and Delta Settings: The configurations can be edited directly in the etl.py script.

