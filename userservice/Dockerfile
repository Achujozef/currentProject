# Use an official Python runtime as a parent image
FROM python:3-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose the port that the Django app will run on
EXPOSE 8001

# Run app.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
