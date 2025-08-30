# python-grpc-services

Template for python grpc services, is a monorepository example

## Project structure
```bash
.
├── product_service
│   ├── __init__.py
│   ...
|   # any other microservice
└── README.md
```

### Microservice structure

Based on example of product_service:

```bash
.
├── __init__.py
├── client
│   └── __init__.py
├── generated
│   ├── __init__.py
│   ├── product_service_pb2_grpc.py
│   └── product_service_pb2.py
├── models
│   └── product.py
├── proto
│   └── product_service.proto
├── requirements.txt
└── server
    ├── __init__.py
    └── server.py
```




