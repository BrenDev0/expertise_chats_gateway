from fastapi import Request, HTTPException, Depends
from src.auth.application.use_cases.validate_token import ValidateToken
from src.auth.dependencies.use_cases import get_validate_token_use_case
from src.auth.domain.exceptions import ExpiredToken, InvalidToken

def auth_middleware(
    request: Request,
    validate_token: ValidateToken = Depends(get_validate_token_use_case)
):
    auth_header = request.headers.get("Authorization", None)
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unautrhorized, Missing required auth headers")

    token = auth_header.split(" ")[1]

    try:
        token_payload = validate_token.execute(token=token)
        user_id = token_payload.get("user_id", None)

        if not user_id:
            raise InvalidToken()
    
    except ExpiredToken:
        raise HTTPException(status_code=403, detail="Expired Token")
    
    except InvalidToken:
         raise HTTPException(status_code=401, detail="Invalid token")
    
    except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))