# Use latest python
FROM python:3.11

# Ensures python output is unbuffered when written out
ENV PYTHONUNBUFFERED 1

# System dependencies
RUN apt-get update && apt-get install -y netcat-traditional

# Create fstore user
RUN useradd -ms /bin/sh fstore

# Add user bin to path
ENV PATH /home/fstore/.local/bin:$PATH

# Create api directory
RUN mkdir /api
RUN mkdir /api/staticfiles

# Set api directory to working directory
WORKDIR /api

# Copy project files to /api
COPY . /api/
COPY ./entrypoint.sh /api/entrypoint.sh
RUN chmod +x /api/entrypoint.sh
RUN chown -R fstore:fstore /api/

# Change to fstore user
USER fstore

# Install requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["./entrypoint.sh"]