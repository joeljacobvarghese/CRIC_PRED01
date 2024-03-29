# CRIC PRED Project

CRIC PRED is a cricket prediction application that combines a FastAPI backend with a React frontend, all containerized using Docker for streamlined setup and deployment.

## Prerequisites

Before starting, ensure you have Docker and Docker Compose installed on your system:

- [Get Docker](https://docs.docker.com/get-docker/)
- [Install Docker Compose](https://docs.docker.com/compose/install/)

## Installation

To set up the CRIC PRED project on your local machine, follow these steps:

1. **Clone the Repository**

```sh
git clone https://github.com/joeljacobvarghese/CRIC_PRED.git
cd CRIC_PRED
```


2. **Build and Run with Docker Compose**

```sh
docker-compose up --build
```

This command builds the Docker images and starts the containers necessary for the CRIC PRED application. The `--build` flag ensures the images are built with the latest version of the source code.

## Usage

After successfully launching the containers, the application will be accessible at:

- **FastAPI Backend:** [http://localhost:8000](http://localhost:8000)
- **React Frontend:** [http://localhost:3000](http://localhost:3000)

Explore the application features by visiting these URLs in your web browser.

## Contributing

Future Goals for CRIC PRED Project:

Contributions to the CRIC PRED project are welcome and appreciated. In addition to the current features, here are some future goals we aim to achieve:

Automated Model Updates:
        Automatically update the prediction model with new cricket game data to ensure predictions are always up-to-date.

Customization via Configuration:
        Introduce a configuration file allowing users to adjust settings like data split for testing and training, and model parameters to suit their needs.

Testing  in CI Pipeline:
        Develop testing suites for both the FastAPI backend and React frontend.

Contributions to the CRIC PRED project are welcome and appreciated. To contribute:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -am 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

