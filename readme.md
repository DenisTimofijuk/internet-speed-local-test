# Speedtest Monitor

## Overview
This project creates a Docker container that runs automated internet speed tests at regular intervals and stores the results in a PostgreSQL database. It's designed to be easily deployable on TrueNAS Scale or any system that supports Docker.

## Purpose
The Speedtest Monitor allows you to:
- Regularly test your internet connection speed
- Store the results (ping, download, and upload speeds) in a database
- Track your internet performance over time

## Components
1. Dockerfile: Defines the Docker image with necessary dependencies
2. speedtest.py: Python script that runs the speed test and logs results
3. PostgreSQL database: Stores the speed test results

## Prerequisites
- Docker
- Access to a PostgreSQL database
- TrueNAS Scale (or any system that can run Docker containers)

## Setup Instructions

### 1. Prepare the files
Create a new directory and add the following files:

- Dockerfile
- speedtest.py

(Contents of these files are provided in the previous messages)

### 2. Build the Docker image
```bash
docker build -t speedtest-monitor .
```

### 3. Ensure you have a PostgreSQL database set up with the following table:
```sql
CREATE TABLE speedtest_results (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    ping FLOAT,
    download FLOAT,
    upload FLOAT
);
```
### 4. Run the Docker container:

```
docker run --name speedtest-monitor -d \
  -e DB_HOST=your_postgres_host \
  -e DB_NAME=your_database \
  -e DB_USER=your_username \
  -e DB_PASSWORD=your_password \
  speedtest-monitor
```
Replace the environment variable values with your actual PostgreSQL connection details.

### 5. Deployment on TrueNAS Scale

1. Use the TrueNAS Scale web interface to create a new Docker image using the provided Dockerfile.
2. Create a new container from this image.
3. Add the following environment variables in the TrueNAS Scale interface:
 - DB_HOST
 - DB_NAME
 - DB_USER
 - DB_PASSWORD
4. Ensure the container has network access to both the internet and your PostgreSQL database.

## Customization

 - To change the frequency of speed tests, modify the schedule.every(1).hour.do(job) line in speedtest.py.
 - Additional metrics or logging can be added by modifying the speedtest.py script.

## Troubleshooting

 - Ensure the container has internet access for running speed tests.
 - Verify that the PostgreSQL connection details are correct and the database is accessible from the container's network.

## Security Notes

 - Database credentials are passed as environment variables to keep them out of the Docker image.
 - Ensure your PostgreSQL database is properly secured and only accessible from trusted networks.

## Contributing
Feel free to fork this project and submit pull requests for any enhancements.

## License
This README provides a comprehensive overview of the project, including setup instructions, deployment guidance for TrueNAS Scale, customization options, and some troubleshooting tips. You may want to adjust some details based on your specific implementation or add more information as needed.# internet-speed-local-test
