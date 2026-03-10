class AppException(Exception):
    def __init__(self, message: str, status_code : int= 400):
        self.message = message
        self.status_code = status_code


# PRODUCT NOT FOUND
class ProductNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            message="The product you are looking for was not found in the system",
            status_code=404
        )


# CART NOT FOUND
class CartNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            message="No such basket was found",
            status_code=404
        )


# OUT OF STOCK 
class OutOfStockException(AppException):
    def __init__(self):
        super().__init__(
            message="Out of stock! Only {stock} units of product '{product_name}' remain",
            status_code=400
        )