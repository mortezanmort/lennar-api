# Stuffs API

Stuffs API is a Django-based application designed to manage Specifications, Groups, and Components. This application allows for creating, updating, and cloning specifications

## Table of Contents

- [Installation & Usage](#installation)
- [Seeding Data](#seeding-data)
- [Feature Documentation](#feature-documentation)
   - [Specifications CRUD](#specifications-crud)
   - [Groups CRUD](#groups-crud)
   - [Components CRUD](#components-crud)
   - [Clone Specifications](#clone-specifications)
   - [Import Specifications](#import-specifications)
   - [Export Built Specifications Report](#export-built-specifications-report)

## Installation

### 1. **Clone the repository**:
```sh
   git clone https://github.com/yourusername/stuffs-api.git
   cd lennar-api
   chmod +x ./bin/**/*
```

### 2. **Use Docker to run the project**
```sh
   docker-compose up -d
```

OR
```sh
./bin/start-all
```
That's all you will be able to access the application at localhost:8000


## Seeding Data
To seed the database with initial data, run the custom Django management command:

This code is supposed to run inside the container
### 3. Connect to Running container
```sh
./bin/app/connect
```
And run
```sh
python manage.py seed_data
```

## CRUD Operations

#### Specifications CRUD

| Method | Endpoint                         | Description                        |
|--------|----------------------------------|------------------------------------|
| GET    | /api/stuffs/                     | API Root                           |
| GET    | /api/stuffs/specifications/      | List all specifications            |
| POST   | /api/stuffs/specifications/      | Create a new specification         |
| GET    | /api/stuffs/specifications/{id}/ | Retrieve a specific specification  |
| PUT    | /api/stuffs/specifications/{id}/ | Update a specific specification    |
| DELETE | /api/stuffs/specifications/{id}/ | Delete a specific specification    |


#### Groups CRUD
| Method | Endpoint                               | Description                            |
|--------|----------------------------------------|----------------------------------------|
| GET   | /api/stuffs/specifications/{id}/groups  | List all groups in specification       |
| POST   | /api/stuffs/specifications/{id}/groups | Create a new group in a specification  |
| GET    | /api/stuffs/groups/{id}/               | Retrieve a specific group              |
| PUT    | /api/stuffs/groups/{id}/               | Update a specific group                |
| DELETE | /api/stuffs/groups/{id}/               | Delete a specific group                |

#### Components CRUD
| Method | Endpoint                                    | Description                                    |
|--------|---------------------------------------------|------------------------------------------------|
| GET   | /api/stuffs/specifications/{id}/components/  | List all Components in specification           |
| POST   | /api/stuffs/specifications/{id}/components/ | Create a new Component in a specification      |
| GET    | /api/stuffs/components/{id}/                | Retrieve a specific Component                  |
| PUT    | /api/stuffs/components/{id}/                | Update a specific Component                    |
| DELETE | /api/stuffs/components/{id}/                | Delete a specific Component                    |

### Implementation

- **Serializers**:
  - `SpecificationSerializer`: Handles the validation and serialization of Specifications.
  - `GroupSerializer`: Handles the validation and serialization of Groups.
  - `ComponentSerializer`: Handles the validation and serialization of Components.

- **Views**:
  - `SpecificationViewSet`: Uses Django Rest Framework's ModelViewSet to handle CRUD operations for specifications.
  - `NestedSpecificationGroupViewSet`: Uses Custom Viewset to provide List and Create operations for *groups in a specification.
  - `NestedSpecificationComponentsViewSet`: Uses Custom Viewset to provide List and Create operations for *Components* in a specification.
  - `GroupViewSet`: Uses Django Rest Framework's ModelViewSet to handle CRUD operations for groups.
  - `ComponentViewSet`: Uses Django Rest Framework's ModelViewSet to handle CRUD operations for components.

## Clone Specifications

### Overview

The cloning feature allows you to create a new specification based on an existing one. Only specifications that are in the "Planning Phase" or "Planning Ready" status can be cloned.

### API Endpoint

| Method | Endpoint                                  | Description                        |
|--------|-------------------------------------------|------------------------------------|
| POST   | /api/stuffs/specifications/{id}/clone/    | Clone a specific specification     |

### Implementation

- **Serializer**:
  - `SpecificationCloneSerializer`: Handles the validation and cloning of specifications.

- **View**:
  - `SpecificationViewSet.clone`: Action in the `SpecificationViewSet` that handles the cloning functionality.

## Import Specifications

### Overview

The import functionality allows you to import specifications, groups, and components from a JSON file. The data is validated and saved in a single transaction to ensure data integrity.

### API Endpoint

| Method | Endpoint                                   | Description                       |
|--------|--------------------------------------------|-----------------------------------|
| POST   | /api/stuffs/specifications/import_data/    | Import specifications, groups, and components from a JSON file |

### Implementation

- **Serializer**:
  - `SpecificationImportSerializer`: Handles the validation and creation of nested specifications, groups, and components.
  - `SpecificationImportExportSerializer`: Used within `SpecificationImportSerializer` to handle nested data validation.

- **View**:
  - `SpecificationViewSet.import_data`: Action in the `SpecificationViewSet` that handles the import functionality.

## Export Built Specifications Report

### Overview

The built specifications report generates a CSV file containing the specification codes and the number of built specifications derived from each `code_number`.

### API Endpoint

| Method | Endpoint                                                      | Description                        |
|--------|---------------------------------------------------------------|------------------------------------|
| GET    | /api/stuffs/specifications/export_built_specification_report/ | Generate a CSV report of built specifications |

### Implementation

- **Model Manager**:
  - `ReportManager.built_count`: Method that groups by `code_number` and counts the number of specifications in the "Built" status for each `code_number`.

- **View**:
  - `SpecificationViewSet.built_specifications_report`: Action in the `SpecificationViewSet` that generates the report using the `built_count` method and uses `pandas` to convert the report data to a CSV file.

## Running Tests

To run the tests, use the following command:

```sh
python manage.py test
