import grpc
from datetime import datetime, timezone
from generated import product_service_pb2
from generated import product_service_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp
from utils.database import is_postgres_healthy

import asyncio
import signal
import settings

# In Memory Database
PRODUCTS = {}
NEXT_ID = 1

def now_ts():
    ts = Timestamp()
    ts.FromDatetime(datetime.now(timezone.utc))
    return ts


class ProductService(product_service_pb2_grpc.ProductServiceServicer):


    async def CreateProduct(self, request, context):
        global NEXT_ID

        product_id = NEXT_ID
        NEXT_ID += 1

        product = product_service_pb2.ProductCreationData(
            product_id=product_id,
            name=request.name,
            brand=request.brand,
            price=request.price,
            category=request.category,
            created_at=now_ts(),
            updated_at=now_ts()
        )

        PRODUCTS[product_id] = product

        return product
    

    async def GetProduct(self, request, context):
        
        product = PRODUCTS.get(request.product_id)

        if not product:

            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Product not found")

            return product_service_pb2.GetProductData()
        
        return product_service_pb2.GetProductData(
            product_id=product.product_id,
            name=product.name,
            price=product.price,
            category=product.category,
            brand=product.brand,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )
    


async def serve():

    if not await is_postgres_healthy(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        database=settings.POSTGRES_DB
    ):
        raise RuntimeError(
            "An error occurred during connection to PostgresDatabase"
        )

    server = grpc.aio.server()
    product_service_pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)
    bound = server.add_insecure_port(f"0.0.0.0:{settings.APP_PORT}")
    if bound == 0:
        raise RuntimeError(f"Failed to bind gRPC on port {settings.APP_PORT}")
    await server.start()
    print(f"[X] Async gRPC server started on port {settings.APP_PORT}")

    stop_event = asyncio.get_event_loop().create_future()

    for sig in (signal.SIGINT, signal.SIGTERM):
        asyncio.get_event_loop().add_signal_handler(sig, stop_event.set_result, None)

    await stop_event

    print("[X] Shutting down gRPC server...")
    await server.stop(grace=5)

if __name__ == "__main__":
    asyncio.run(serve())