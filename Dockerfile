# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the application source code into the container
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Run the Streamlit app when the container starts
CMD ["streamlit", "run", "src/app.py"]
