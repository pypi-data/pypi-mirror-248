"""
响应工具
"""
import json
from typing import Any

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.responses import JSONResponse, FileResponse, Response, RedirectResponse

from afeng_tools.sqlalchemy_tool.core import sqlalchemy_model_utils
from afeng_tools.sqlalchemy_tool.core.sqlalchemy_base_model import Model
from afeng_tools.web_tool.core.web_common_models import ResponseModel


def create_json_response_data(data: Any = None, error_no: int = 0, message: str = 'success') -> ResponseModel:
    # if isinstance(data, Model) or (data and isinstance(data, list) and len(data) > 0 and isinstance(data[0], Model)):
    #     data = json.loads(sqlalchemy_model_utils.to_json(data))
    # if isinstance(data, BaseModel):
    #     data = data.model_dump(mode='json')
    return ResponseModel(
        error_no=error_no,
        message=message,
        data=jsonable_encoder(data)
    )


def create_json_response(response_model: ResponseModel) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content=response_model.model_dump(mode='json')
    )


def json_response(data: Any = None, error_no: int = 0, message: str = 'success') -> JSONResponse:
    response_model = create_json_response_data(data=data, error_no=error_no, message=message)
    return create_json_response(response_model=response_model)


