import re
from typing import List, Callable, Literal
from urllib.parse import unquote_plus

from fastapi import Request
from pydantic import BaseModel
from sqlalchemy.sql.base import ReadOnlyColumnCollection
from sqlalchemy.sql.expression import desc, asc
from sqlmodel import SQLModel
from sqlmodel.main import SQLModelMetaclass


class Order(BaseModel):
    """ 排序 """
    sortField: str
    sortType: Literal["descending", "ascending"]


class OrderParams(BaseModel):
    order: List[Order]
    order_by: Callable


def parse_order_arguments(request: Request) -> List[Order]:
    """ 解析前端排序参数 """

    def parse_order(order_param: str) -> List[Order]:
        order_param = unquote_plus(order_param)
        order_field_values = re.findall(r'sort\[\d+\]\.sortField=([\w]+)', order_param)
        order_type_values = re.findall(r'sort\[\d+\]\.sortType=([\w]+)', order_param)

        result = [
            Order(sortField=s_field, sortType=s_type)
            for s_field, s_type in
            zip(order_field_values, order_type_values)
        ]
        return result

    order_params = parse_order(str(request.query_params))

    def order_by(model_or_column: SQLModel | ReadOnlyColumnCollection):
        order_bys = []
        if isinstance(model_or_column, SQLModelMetaclass):
            columns = model_or_column.__table__.columns
        else:
            columns = model_or_column

        for order_param in order_params:
            if order_param.sortType == "descending":
                order_clause = desc(columns[order_param.sortField])
            else:
                order_clause = asc(columns[order_param.sortField])
            order_bys.append(order_clause)
        return order_bys

    return OrderParams(order=order_params, order_by=order_by)
