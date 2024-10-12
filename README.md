# FastAPI Project - User Clock-In Records and Items Management

This is a FastAPI-based project that provides APIs to manage **User Clock-In Records** and **Items**. You can create, retrieve, update, delete, and filter records for both items and user clock-ins.

## Deployed API

You can access the deployed API at the following link:

[https://vodex-items-clockin-api.onrender.com](https://vodex-items-clockin-api.onrender.com)

API documentation is available at:

[https://vodex-items-clockin-api.onrender.com/docs](https://vodex-items-clockin-api.onrender.com/docs)

## Pre-requisites

Make sure you have the following installed:

- **Python 3.12**
- **MongoDB** (local or MongoDB Atlas) 
- **Git** (for cloning the repository)

## Project Setup

### Clone the Repository

First, clone the repository to your local machine:

```bash
git clone "https://github.com/ariwalapratham/Vodex-Items-ClockIn-API.git"
cd Vodex-Items-ClockIn-API
```

## Environment Setup

### 1. Create a Virtual Environment

It is recommended to create a virtual environment to isolate dependencies.

#### Ubuntu/Linux/macOS:
```bash
# Install virtualenv if not already installed
pip install virtualenv

# Create a virtual environment
python3.12 -m venv env

# Activate the virtual environment
source env/bin/activate
```

#### Windows:
```bash
#Install virtualenv if not already installed
pip install virtualenv

# Create a virtual environment
python -m venv env

# Activate the virtual environment
env\Scripts\activate
```

### 2. Add Your MongoDB Connection String
Create a ```.env``` file and add your MongoDB connection string (local or mongodb atlas)and database name. The file should look like this:
```bash
MONGODB_URL="your_mongodb_connection_string"
DATABASE_NAME="your_db_name"
```

### 3. Install Dependencies

After activating the virtual environment, install the required dependencies from **requirements.txt**:
```bash
pip install -r requirements.txt
```
This will install all the necessary Python packages for the project.

### 4. Running the Server
After setting up the environment and installing dependencies, you can run the FastAPI server.

```bash
uvicorn app.main:app --reload
```
The server will start on http://127.0.0.1:8000 by default. Use the --reload flag to enable hot-reloading during development.

### 5. Access the API
Open your browser and navigate to http://127.0.0.1:8000/docs to view the interactive API documentation provided by Swagger UI.


## Endpoints

### Items Endpoints

1. **POST /items**
   - **Description**: Creates a new item in the database. This endpoint requires information about the item, including the name of the user, their email, the name of the item, the quantity, and the expiry date. Upon successful creation, the server returns the newly created item's details, including an automatically generated insert date.

2. **GET /items/{id}**
   - **Description**: Retrieves the details of a specific item based on its unique identifier (ID). If the item exists, the server returns its details. If not, a 404 error is returned.

3. **PUT /items/{id}**
   - **Description**: Updates the details of an existing item identified by its ID. The request body should include the updated information for the item. Upon a successful update, the server returns the updated item details.

4. **DELETE /items/{id}**
   - **Description**: Deletes an item from the database based on its ID. If the item is successfully deleted, the server responds with a 204 No Content status, indicating the operation was successful.

5. **GET /items/filter**
   - **Description**: Filters item records in the database based on various query parameters, including the user's email, expiry date, insert date, and quantity. Users can specify one or more filters to narrow down the results. Additionally, if the `aggregate` query parameter is set to `true`, the endpoint performs an aggregation operation to count the number of items grouped by email. The server returns either a list of filtered item records or the aggregated counts, depending on the request parameters.


### User Clock-In Records Endpoints

1. **POST /clock-in**
   - **Description**: Creates a new clock-in record for a user. The request must include the user's email and location. Upon successful creation, the server returns the details of the newly created clock-in record, including an automatically generated insert date.

2. **GET /clock-in/{id}**
   - **Description**: Retrieves the details of a specific clock-in record based on its unique identifier (ID). If the record exists, the server returns its details; if not, a 404 error is returned.

3. **GET /clock-in/filter**
   - **Description**: Filters clock-in records in the database based on specified query parameters such as email, location, and insert date. The server returns a list of clock-in records that match the provided criteria.

4. **DELETE /clock-in/{id}**
   - **Description**: Deletes a clock-in record from the database based on its ID. If the record is successfully deleted, the server responds with a 204 No Content status.

5. **PUT /clock-in/{id}**
   - **Description**: Updates an existing clock-in record identified by its ID. The request body should include the updated email and/or location. Upon a successful update, the server returns the updated clock-in record details.