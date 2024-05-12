# Use an official Python runtime as a parent image with Java installed
FROM openjdk:8-jdk

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Python and pip
# RUN apk add --no-cache python3 py3-pip bash && \
#     python3 -m ensurepip && \
#     pip3 install --upgrade pip
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/bin/python3 /usr/bin/python


# Set JAVA_HOME environment variable
# ENV JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk
# ENV PATH="$JAVA_HOME/bin:${PATH}"

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip3 install  -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY src/ /app/src/
COPY features/ /app/features/
COPY data/data.csv /app/data/data.csv


WORKDIR /app

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set the default command to use the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["app"]
