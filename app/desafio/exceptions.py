from rest_framework import status

class NotFoundException(Exception):
    def __init__(self, message="Not Found", *args, **kwargs):
        self.message = message
        self.code = status.HTTP_404_NOT_FOUND
        
class UnprocessableEntityException(Exception):
    def __init__(self, message="Unprocessable Entity", errors=[], *args, **kwargs):
        self.message = message
        self.errors = errors
        self.code = status.HTTP_422_UNPROCESSABLE_ENTITY
        
class InternalServerException(Exception):
    def __init__(self, message="Internal Server Error", *args, **kwargs):
        self.message = message
        self.code = status.HTTP_500_INTERNAL_SERVER_ERROR