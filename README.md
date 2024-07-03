# Stuffs API

Stuffs API is a Django-based application designed to manage Specifications, Groups, and Components. This application allows for creating, updating, and cloning specifications

## Table of Contents

- [Installation & Usage](#installation)
- [Seeding Data](#seeding-data)
- [API Endpoints](#api-endpoints)

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

## API Endpoints
### API Endpoints

| Method | Endpoint                                                | View                                        | Name                            |
|--------|---------------------------------------------------------|---------------------------------------------|---------------------------------|
| GET    | /api/stuffs/                                             | rest_framework.routers.APIRootView          | api-root                        |
| GET    | /api/stuffs/components/\<pk\>/                            | stuffs.viewsets.ComponentViewSet            | component-detail                |
| PATCH  | /api/stuffs/components/\<pk\>/assign_part/                | stuffs.viewsets.ComponentViewSet            | component-assign-part           |
| GET    | /api/stuffs/groups/\<pk\>/                                | stuffs.viewsets.GroupViewSet                | group-detail                    |
| GET    | /api/stuffs/specifications/                               | stuffs.viewsets.SpecificationViewSet        | specification-list              |
| POST   | /api/stuffs/specifications/                               | stuffs.viewsets.SpecificationViewSet        | specification-list              |
| GET    | /api/stuffs/specifications/\<pk\>/                        | stuffs.viewsets.SpecificationViewSet        | specification-detail            |
| PUT    | /api/stuffs/specifications/\<pk\>/                        | stuffs.viewsets.SpecificationViewSet        | specification-detail            |
| PATCH  | /api/stuffs/specifications/\<pk\>/                        | stuffs.viewsets.SpecificationViewSet        | specification-detail            |
| DELETE | /api/stuffs/specifications/\<pk\>/                        | stuffs.viewsets.SpecificationViewSet        | specification-detail            |
| POST    | /api/stuffs/specifications/\<pk\>/clone                  | stuffs.viewsets.SpecificationViewSet        | specification-detail            |
| GET    | /api/stuffs/specifications/\<specification_pk\>/components/ | stuffs.viewsets.NestedSpecificationComponentsViewSet | specification-components-list  |
| POST   | /api/stuffs/specifications/\<specification_pk\>/components/ | stuffs.viewsets.NestedSpecificationComponentsViewSet | specification-components-list  |
| GET    | /api/stuffs/specifications/\<specification_pk\>/groups/   | stuffs.viewsets.NestedSpecificationGroupViewSet | specification-groups-list      |
| POST   | /api/stuffs/specifications/\<specification_pk\>/groups/   | stuffs.viewsets.NestedSpecificationGroupViewSet | specification-groups-list      |
