import json
from typing import List
from products import Product, get_product
from cart import dao


class Cart:
    def _init_(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> 'Cart':
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> List[Product]:
    """
    Retrieve the cart for a given username and return the product details.
    """
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    product_ids = []
    for cart_detail in cart_details:
        # Safely deserialize contents instead of using eval
        contents = json.loads(cart_detail.get('contents', '[]'))
        product_ids.extend(contents)

    # Fetch product details for all items in the cart
    products_in_cart = [get_product(product_id) for product_id in product_ids]
    return products_in_cart


def add_to_cart(username: str, product_id: int):
    """
    Add a product to the user's cart.
    """
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    """
    Remove a specific product from the user's cart.
    """
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    """
    Delete the entire cart for the given username.
    """
    dao.delete_cart(username)