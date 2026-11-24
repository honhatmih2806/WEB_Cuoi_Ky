from fastapi import HTTPException

class AppException(HTTPException):
    def __init__(self, code: str, message: str, status_code: int = 400, details: any = None):
        super().__init__(status_code=status_code, detail={"code": code, "message": message, "details": details})
        self.code = code
        self.message = message
        self.details = details
