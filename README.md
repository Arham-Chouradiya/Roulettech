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


## AWS Architecture Diagram Description
In this 3-tier AWS architecture diagram for the TicketMaster web app, the architecture begins with Amazon Route 53 positioned at the top left corner. Route 53 handles DNS routing, directing user traffic to Amazon CloudFront, which is placed slightly lower and to the right. CloudFront acts as a content delivery network, optimizing the distribution of static files stored in Amazon S3, which is directly below CloudFront. Traffic for dynamic content is then sent to the AWS Elastic Load Balancer, positioned in the center to the right of CloudFront, which evenly distributes incoming requests across multiple Amazon EC2 instances located to its right. These EC2 instances host the Django application, handling interactions with external APIs like TicketMaster and Spotify, and managing application logic. To the right of the EC2 instances, Amazon RDS is placed as the relational database service, responsible for storing user data, such as favorite events. Below RDS, another Amazon S3 instance is used for storing backups of the database. Optional components like Amazon ElastiCache, which could be used to cache frequent API responses, and Amazon DynamoDB, for managing NoSQL data, have not been included in this configuration but could be positioned below the EC2 instances and to the left of RDS, respectively, if needed.
