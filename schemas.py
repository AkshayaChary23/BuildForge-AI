from pydantic import BaseModel
from typing import List, Dict


class Page(BaseModel):
    name: str
    route: str
    components: List[str]


class APIEndpoint(BaseModel):
    path: str
    method: str
    entity: str


class Table(BaseModel):
    name: str
    fields: Dict[str, str]


class Role(BaseModel):
    name: str
    permissions: List[str]


class AppConfig(BaseModel):
    app_name: str
    assumptions: List[str]
    pages: List[Page]
    api_endpoints: List[APIEndpoint]
    database_tables: List[Table]
    roles: List[Role]
    business_logic: List[str]