# AMQP-restapi
A simple restapi for sending messages to an ampq based message broker

This app is a simple REST API that allows you to send messages to an AMQP-based message broker.  based on aiopika and
FastAPI.

This was designed to be used with RabbitMQ, but likely will work with any AMQP-based message broker.

## Usage
### Dependencies
- Python 3.11+
- pip

### Environment Variables
- `RPC_URI`: The URI of the message broker. E.G `amqp://guest:guest@localhost:5672/`

### Docker
You can run the container by pulling from Github container registry
```bash
docker run ghcr.io/iplsplatoon/AMQP-restapi:master -p 2000:2000 -e RPC_URI=amqp://guest:guest@localhost:5672/
```

or use `ghcr.io/iplsplatoon/ampq-restapi:master` as the image name in your docker-compose file.

Example `docker-compose` file:
```yaml
services:
    rabbitmq:
        image: rabbitmq:3-management-alpine
        restart: unless-stopped
        container_name: 'rabbitmq'
        ports:
            - "5672:5672"
            - "15672:15672"
        volumes:
            - ./volumes/rabbitmq/data/:/var/lib/rabbitmq/
            - ./volumes/rabbitmq/log/:/var/log/rabbitmq
    rest-amqp:
      image: b9d1a35b
      ports:
        - "2000:2000"
      environment:
        RPC_URI: amqp://guest:guest@rabbitmq:5672
```

### Install: Bare Metal
You can run the application using the Fastapi CLI

1. Install python dependencies with pip
    ```bash
    pip install -r requirements.txt
    ```

2. Run the application
    ```bash
    fastapi dev restapi/main.py 
    ```
   
#### Ports
The application will run on port `2000` by default. In docker you can change this by changing the `-p` flag in the 
docker run command or in your docker-compose file. For bare metal, you can change the port by using the `--port`
   
### Making requests

#### Docs
The application is documented using OpenAPI. 
You can view the documentation by navigating to `http://localhost:2000/docs` in your web browser.

#### Send a message
You can make a **POST** request to the `/rpc/response` endpoint with the following query parameters:

- `routing_key`: The routing key to use for the message. This is a required parameter.
- `timeout`: The timeout for the request in seconds. (Default: Never)

You message body should be what ever you want to be sent, the app will convert this to a byte string and send it as the
message body. We also use the `content_type` header to set the content type of the message that send to the message broken.

The response will be send back to what ever client you using back and will forward the body, headers and other 
properties from the response message.

_If you don't need a response, you can use the `/rpc/one_way` endpoint instead._

## Development

### Dependencies
PDM is used for dependency management. 

To install dependencies, run the following command:
```bash
pdm install
```

### Linting
We use `ruff` for linting and formatting. You can run the following command to lint and format the code:
```bash
ruff check
ruff format
```