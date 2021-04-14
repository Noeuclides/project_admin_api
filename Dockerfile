FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CONTAINER_RUNNING Yes

# Create a working directory for the django project
WORKDIR /code

# Copy requirements to the container
COPY Pipfile Pipfile.lock /code/

# Install the requirements to the container
RUN pip install pipenv && pipenv install --system

# Copy the project files into the working directory
COPY . /code/

# Open a port on the container
EXPOSE 8000
