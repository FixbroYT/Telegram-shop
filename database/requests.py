import logging
import os

from sqlalchemy import select

from database.models import async_session, Product

logger = logging.getLogger(__name__)

async def create_product(product_name: str, product_price: float, product_image_url: str):
    async with async_session() as session:
        products = await session.scalars(select(Product).where(Product.name == product_name.lower()))

        if products.all():
            logger.error("The new product is not saved to the database because there is already a product with the same name")
            return

        new_product = Product(name=product_name.lower().strip(), price=product_price, image=product_image_url)
        session.add(new_product)
        await session.flush()
        await session.commit()
        logger.info("The new product is saved to database")
        return True

async def get_all_products():
    async with async_session() as session:
        products = await session.scalars(select(Product))
        products = products.all()

        if not products:
            logger.warning("There are no products in the database at the moment")
            return

        json_response = []

        for product in products:
            json_response.append(
                {
                    "name": product.name,
                    "price": product.price,
                    "image": product.image
                }
            )

        return json_response

async def delete_product(product_name: str):
    async with async_session() as session:
        product = await session.scalar(select(Product).where(Product.name == product_name.lower()))

        if not product:
            logger.error("Product not found in the database")
            return

        os.remove(f"static/images/{product.image}")

        await session.delete(product)
        await session.flush()
        await session.commit()
        logger.info("The product has been successfully removed")
        return True


async def get_products_from_db(products: list[str]):
    async with async_session() as session:
        db_products = []

        for product in products:
            db_product = await session.scalar(select(Product).where(Product.name == product.lower()))

            if not db_product:
                logger.error("Product not found in the database")
                return

            db_products.append(db_product)

        return db_products