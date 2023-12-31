from __future__ import annotations

import datetime
import pydantic
import typing

from pydantic import BaseModel

from feedancy.lib.base import BaseApi
from feedancy.lib.request import ApiRequest
from feedancy.lib import json
class StopKeyword(BaseModel):
    name: str 

class SearchKeyword(BaseModel):
    name: str 
    slug: str 
    stop_keywords: typing.List[StopKeyword] 

class PaginatedSearchKeywordListData(BaseModel):
    next: typing.Optional[typing.Union[int, None]]  = None
    results: typing.Optional[typing.List[SearchKeyword]]  = None

class PaginatedSearchKeywordList(BaseModel):
    data: typing.Optional[PaginatedSearchKeywordListData]  = None
    error: typing.Optional[str]  = None

def make_request(self: BaseApi,

    __request__: typing.List[SearchKeyword],


    page: int = ...,

) -> PaginatedSearchKeywordList:
    

    
    body = __request__
    

    m = ApiRequest(
        method="POST",
        path="/api/v1/keywords/".format(
            
        ),
        content_type="application/json",
        body=body,
        headers=self._only_provided({
        }),
        query_params=self._only_provided({
                "page": page,
            
        }),
        cookies=self._only_provided({
        }),
    )
    return self.make_request({
    
        "201": {
            
                "application/json": PaginatedSearchKeywordList,
            
        },
    
    }, m)