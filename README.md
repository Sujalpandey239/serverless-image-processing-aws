🚀 AWS Serverless Image Processing Pipeline
Internship Project 
A fully automated, event-driven image manipulation service built using AWS Lambda, Amazon S3, and API Gateway. This project demonstrates a production-ready serverless architecture for handling media assets.

📖 Project Overview
This pipeline automates the workflow of resizing and branding images. It is designed to be highly scalable and cost-effective, running entirely within the AWS Free Tier. It supports two distinct triggers:

Event-Driven: Automatically processes images uploaded to an S3 bucket.

REST API: Processes specific images via an HTTP POST request using API Gateway and Postman.

🛠️ Tech Stack
Cloud Provider: AWS (Amazon Web Services)

Compute: AWS Lambda (Python 3.12)

Storage: Amazon S3 (Input & Output Buckets)

API Layer: Amazon API Gateway (REST API)

Messaging: Amazon SNS (Email Notifications)

Image Engine: Pillow (PIL) via Lambda Layers

✨ Key Features
Multi-Size Generation: Automatically creates Thumbnail, Medium, and Large variants for every upload.

Dynamic Watermarking: Applies a custom branded watermark: "Sujal | AWS Project".

Professional Configuration: Uses Environment Variables to decouple code from infrastructure (Industry Best Practice).

Real-time Alerts: Sends instant email notifications via SNS upon successful processing.

📂 Repository Structure
lambda_function.py: The core Python logic for image processing.

week 1 complete.pdf: Detailed report on S3 & Lambda setup.

week 2 complete.pdf: Detailed report on API Gateway & SNS integration.

screenshots/: Folder containing visual proof of the working pipeline.

🚀 How it Works
An image is uploaded to the sujal-input-images bucket or a POST request is sent via API Gateway.

AWS Lambda is triggered and downloads the image.

The image is resized into three versions, watermarked, and uploaded to sujal-output-images.

A notification is sent to the administrator's email via SNS.

🏆 Project Achievements
Successfully maintained Zero-Cost operation using AWS Free Tier.

Implemented Least Privilege IAM Roles for security.

Developed a "Universal Trigger" handler to manage multiple event sources.
