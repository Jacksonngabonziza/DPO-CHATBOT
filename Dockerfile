# Use official Rasa SDK image
FROM rasa/rasa:3.5.0

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install additional dependencies if any
RUN pip install --no-cache-dir -r requirements.txt

# Expose Rasa port (default is 5005)
EXPOSE 5005

# Start Rasa server
CMD ["run", "--enable-api", "--cors", "*", "--debug"]
