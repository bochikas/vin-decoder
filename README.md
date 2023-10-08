# VIN Decoder API

The VIN Decoder API is a web application that provides information about vehicles based on their Vehicle Identification Number (VIN). This project is built using FastAPI and PostgreSQL.

## Installation

To install and run the project, follow these steps:

1. Clone the repository:

```shell
git clone https://github.com/bochikas/vin-decoder.git
cd vin-decoder-api
```
2. Create a .env file in the project's root directory and specify your PostgreSQL database settings and VIN service URL:
```dotenv
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
DB_NAME=your_db_name
VIN_SERVICE_URL=your_vin_service_url
```
3. Запустить docker-compose:
```shell
docker-compose up -d --build
```
4. Run database migrations:
```shell
docker-compose exec app alembic upgrade head
```

## Usage
After installing and running the application, you can use it to retrieve information about vehicles based on their VIN.

### Request
Make a GET request to `/api/v1/vehicles/decode/{vin}/`, where `{vin}` is the Vehicle Identification Number (VIN) of the vehicle.

Example request:
```shell
curl -X GET "http://127.0.0.1:8000/api/v1/vehicles/decode/1P3EW65F4VV300941/"
```

### Response
On a successful request, you will receive vehicle information in JSON format:
```json
{
    "id": 1,
    "year": 2003,
    "make": "Honda",
    "model": "Accord",
    "type": "Sedan",
    "color": "Blue",
    "weight": 1500.0
}
```