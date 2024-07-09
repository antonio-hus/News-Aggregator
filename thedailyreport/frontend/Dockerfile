# Use the official Node.js image as the base image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json into the working directory
COPY package*.json ./

# Install the project dependencies
RUN npm install
RUN npm install -g serve

# Copy the rest of the application code into the working directory
COPY . .

# Build the React application for production
RUN npm run build

# Set the command to serve the application
CMD ["npx", "serve", "-s", "build"]

# Expose port 5000 (adjust as needed based on your application)
EXPOSE 5000
