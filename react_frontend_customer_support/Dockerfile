# Use an official Node.js runtime as a parent image
FROM node:16

# Set work directory
WORKDIR /app

# Copy package.json and install npm dependencies
COPY package.json /app/
COPY package-lock.json /app/
RUN npm install

# Copy the entire React frontend code
COPY . /app/

# Expose port 5000
EXPOSE 5000
