# Use an official Python runtime as a parent image
FROM python:3

# Set environment variables for Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE "techschool.settings"
ENV ALLOWED_HOSTS ""

# Set the working directory in the container
WORKDIR /minsocial

# Copy the requirements file into the container
COPY requirements.txt /minsocial/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /minsocial/

# Expose the port that the Django development server will run on
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
