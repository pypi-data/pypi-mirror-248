import json
from rmbcommon.models.base import BaseCoreModel

class BIQuestion:

    def __init__(self, content):
        self.content = content

    def __str__(self):
        return self.content

class BIQueryPlan:
    pass


class NaturalQuery:

    def __init__(self, content: str):
        self.content = content

    def __str__(self):
        return self.content


class StrucQuery:

    def __init__(self, content: str, params: dict = None):
        self.content = content
        self.params = params or {}

    def __str__(self):
        return self.content

    def __repr__(self):
        return self.__str__()

    @property
    def params_for_query(self):
        # 用于查询的参数
        return {key: value["value"] for key, value in self.params.items()}


class QueryResult:

    def __init__(self, content: any):
        self.content = content

    def __str__(self):
        # 使用这个方法读取content
        raise NotImplementedError

    def __repr__(self):
        return self.__str__()


class BIAnswer(BaseCoreModel):
    __init_dict_keys__ = ['status', 'elapsed_time', 'answer', 'structure_queries']

    def __str__(self):
        return f"[{self.status}-{self.elapsed_time}s] {self.answer}"

    def __repr__(self):
        return self.__str__()

