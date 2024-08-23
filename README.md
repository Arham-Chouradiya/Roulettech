# TicketMaster Web App

## Overview

This web application allows users to search for events using the TicketMaster API, view event details, and manage favorite events. Built with Django for the backend and a modern frontend stack, this app demonstrates a complete solution for integrating external APIs and handling user data.

## Features

- **Search Events**: Users can search for events by keyword, distance, category, and location.
- **Event Details**: View detailed information about each event, including venue details and artist information (integrated with Spotify API).
- **Favorites**: Users can mark events as favorites, which are stored in local storage for easy access.

## Architecture

The application is structured using a 3-tier architecture:

1. **Presentation Layer**:
   - **Amazon S3**: Hosts static files like HTML, CSS, and JavaScript.
   - **Amazon CloudFront**: Delivers content with low latency.
   - **Amazon Route 53**: Manages DNS routing.

2. **Application Layer**:
   - **Amazon EC2**: Hosts the Django application.
   - **AWS Elastic Load Balancer**: Distributes traffic across EC2 instances.
   - **Amazon Auto Scaling**: Adjusts EC2 instances based on load.
   - **Amazon ElastiCache** (optional): Caches API responses.

3. **Data Layer**:
   - **Amazon RDS**: Manages relational database for storing user data.
   - **Amazon DynamoDB** (optional): Stores NoSQL data.
   - **Amazon S3**: Stores backups and logs.
