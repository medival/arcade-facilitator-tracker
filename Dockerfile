# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED True

# Install Chrome dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN curl -sS -L -o /tmp/google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get -y install /tmp/google-chrome.deb \
    && rm /tmp/google-chrome.deb

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` \
    && curl -sS -L -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver_linux64.zip

# Install application dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application files
COPY . /app
WORKDIR /app

# Command to run the application
CMD exec gunicorn --bind :$PORT --workers $GUNICORN_PROCESSES --threads $GUNICORN_THREADS --timeout 120 app:app
