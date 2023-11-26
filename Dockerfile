# Use an official Python runtime as a parent image
FROM python:3.11-slim
# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Run the command to install any necessary dependencies
RUN pip install --no-cache-dir -U lodestone gradio==3.*
ENV NODE_VERSION=18.18.2
RUN apt-get update
RUN apt-get -qq -y install curl
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
EXPOSE 8000
EXPOSE 5000
EXPOSE 5001
EXPOSE 5002
CMD ["python", "main.py"]