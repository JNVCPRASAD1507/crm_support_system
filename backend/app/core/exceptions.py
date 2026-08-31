from fastapi import HTTPException, status
def bad_request(detail): raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
def forbidden(detail="Not enough permissions"): raise HTTPException(status_code=403, detail=detail)
def not_found(detail="Resource not found"): raise HTTPException(status_code=404, detail=detail)
