###############################################
#	METADATA ---->
#
#	NAME: MD SAUBAN KHAN
#	Org: Student
#	Date/Time : Dec 01, 2014 @ 15:00 hr IST
#	Version: v2 (updated for showing metrics @localhost:8000/metrics endpoint)
#
###############################################

################################################# 
#
# This is the Multi-stage Dockerfile for a simple static web-page
# that uses Django Framefork to run the Development server
# It reduces image size by separating the build and runtime stages
#
# The Project file is located in test-webpage/devops/devops/app
#
##################################################

# Stage 1: Build stage with all necessary build dependencies
FROM python:3.11-slim AS builder

WORKDIR /webpage

# Copy requirements.txt and install dependencies
COPY requirements.txt /webpage

# Install the necessary build tools and Python packages
RUN apt-get update && \
    apt-get install -y gcc libpq-dev python3-dev && \
    pip install --no-cache-dir -r requirements.txt --break-system-packages

# Stage 2: Final image (runtime)
FROM python:3.11-slim

WORKDIR /webpage

# Copy only the essential files from the builder image to the runtime image
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY devops /webpage

# Expose the necessary port
EXPOSE 8000

# Entry point for Django application
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

