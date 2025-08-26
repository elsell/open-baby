# Builder stage
FROM node:20-slim AS builder

# Set working directory
WORKDIR /app

# Switch to root user for installation
USER root

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Build the application
RUN npm run build

# Runtime stage
FROM cgr.dev/chainguard/node:latest

# Set working directory
WORKDIR /app

# Copy built application from builder
COPY --from=builder /app/.output ./.output

# Expose the port
EXPOSE 3000

# Start the application
ENTRYPOINT ["node", "/app/.output/server/index.mjs"]