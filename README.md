# ampq-restapi
A simple restapi for sending messages to an ampq based message broker

This app is a simple REST API that allows you to send messages to an AMQP-based message broker.  based on aiopika and
FastAPI.

This was designed to be used with RabbitMQ, but likely will work with any AMQP-based message broker.

## Usage
### Dependencies
- Python 3.11+
- pip

### Environment Variables
- `RPC_URI`: The URI of the message broker. E.G `amqp://guest:guest@localhost/`
- `PORT`: The port to run the application on. (Default: 2000)

### Docker
You cause pull the container from Github container registry
```bash
docker pull ghcr.io/iplsplatoon/ampq-restapi:master
```

or use `ghcr.io/iplsplatoon/ampq-restapi:master` as the image name in your docker-compose file.

### Install: Bare Metal
1. Install python dependencies with pip
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application
    ```bash
    python -m restapi
    ```
   
### Making requests
The application will run on port 2000 by default.

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