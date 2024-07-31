# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# Create a requirements.txt file if you don't have one yet
RUN pip install --no-cache-dir streamlit chromadb pandas

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run the Streamlit app when the container launches
CMD ["streamlit", "run", "chroma_db_viewer.py"]
