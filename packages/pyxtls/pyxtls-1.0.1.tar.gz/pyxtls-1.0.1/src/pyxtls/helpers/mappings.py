# -*- coding:utf-8 -*-
# author: HPCM
# time: 2022/1/14 10:27
# file: mappings.py
import re
import json
from collections import UserDict


class Data(object):
    regex = re.compile("//.*?\n")

    @classmethod
    def load(cls, filename):
        with open(filename, encoding="utf-8") as fp:
            content = cls.regex.sub("\n", fp.read().replace("'", "\"").replace("\r", "").replace("\n\n", "\n"))
            return json.loads(content.replace("//", r"\/\/"))

    @classmethod
    def dump(cls, obj, filename):
        with open(filename, "w+", encoding="utf-8") as fp:
            fp.write(cls.dumps(obj))

    @classmethod
    def dumps(cls, obj):
        return json.dumps(obj, ensure_ascii=False, cls=json.JSONEncoder)


class Parse(object):
    parse_field = "parse__"

    def __init__(self, data):
        self.data = data

    def parse(self):
        [m.startswith(self.parse_field) and getattr(self, m)() for m in dir(self)]
        return self.data


class ParseDict(UserDict):
    """
    将深度数据偏平化处理
    ! 表示开启映射关系
        {"a": 1, "b": 2, "c": {"d": 4}}  mappings = {"!a": "!c:d"}  ==> {1: 4}
        {"a": 1, "b": 2}   mappings = {"a": "!c:d"}  ==> {"a": 4}

    * 表示统配当前key
        {"1": {"a": 1}, "2": {"a": 2}} mappings = {"a": "!*:a} ==> {"a": [1, 2]}
    @ 表示当前节点为list, 但是还需要迭代降维处理
        {"1": [{"b": 1}], "2": [{"b": 2}]} mappings = {"a": "!*:@:b"} ==> {"a": [1, 2]}
    : 表示深度递归使用的分隔符号,
        {"a": {"b": {"c": 1}}}  mappings = {"a": "!a:b:c"} ==> {"a": 1}
    , 表示联合输出为dict
    a|b 将b的数据命名为a
        {"a": {"b": 1, "c": 2}}}   mappings = {"a": "!a:e|b,d|f"} ==> {"a": {"e": 1, "d": 2}}

    __init__(self, data)
    :param data: dict, 需要操作的字典, 最终返回dict, 和add_iter_data互斥, 只能二选一

    add_iter_data(data): 选填
    :param data: list(dict),  迭代映射 parse() 最终将返回一个list

    add_mappings(mappings):  必填
    :param mappings: dict, 添加映射规则

    add_callback(data):  选填
    :param data: list(dict), 添加回调映射
        [{
            "field": lambda x: x   回调函数, 接受一个解析后的结果, 并在mappings中增加field=函数返回值
        }]
    """
    item_mappings = {}
    callbacks = []
    parser = None
    iter_data = []
    iter_status = False

    def __getitem__(self, item):
        return self.get(item)

    def add_mappings_file(self, filename):
        self.item_mappings = Data.load(filename)
        return self

    def add_callback(self, callback=None, parser=None):
        self.callbacks = callback
        self.parser = parser
        return self

    def add_mappings(self, item_mappings):
        self.item_mappings = item_mappings
        return self

    def add_iter_data(self, iter_data):
        self.iter_data = iter_data
        self.iter_status = True
        return self

    def parse_dict_to_list(self, vl, vd, v):
        vl.append(v)

    def parse_dict_auto(self, vl, vd, v):
        if isinstance(v, list):
            vl += v
        elif isinstance(v, dict):
            vd.update(v)
        else:
            vl.append(v)

    def parse_list_auto(self, vl, vd, v):
        if isinstance(v, list):
            vl += v
        elif isinstance(v, dict):
            vl.append(v)
        else:
            vl.append(v)
        return vl or vd

    def parse_any_key(self, i, v_data, fields, field):
        vl, vd = [], {}
        for data in v_data.values():
            if data:
                v = self.depth_handle(data, fields[i + 1:])
                if v:
                    if field == "*":
                        self.parse_dict_auto(vl, vd, v)
                    elif field == "*@":
                        self.parse_dict_to_list(vl, vd, v)
                    else:
                        raise KeyError
        return vl or vd

    def parse_list(self, i, v_data, fields, field):
        vl, vd = [], {}
        for data in v_data:
            if data:
                v = self.depth_handle(data, fields[i + 1:])
                if v:
                    if field == "@":
                        self.parse_list_auto(vl, vd, v)
                    else:
                        raise KeyError
        return vl or vd

    def depth_handle(self, v_data, fields, tran_dict=json.JSONEncoder):
        if not isinstance(v_data, (list, tuple, dict, str, set, bool)):
            v_data = tran_dict().encode(v_data)
        for i, field in enumerate(fields):
            if field.startswith("*"):
                v_data = self.parse_any_key(i, v_data, fields, field)
                break
            elif field.startswith("@"):
                v_data = self.parse_list(i, v_data, fields, field)
                break
            elif "," in field:
                items = {}
                [items.update(self.depth_handle(v_data, [x] + (fields[i + 1:]))) for x in field.split(",") if x]
                v_data = items
                break
            elif "|" in field:
                k, v = field.split("|")
                v_data = {k: self.depth_handle(v_data, [v])}
                break
            else:
                if isinstance(v_data, dict):
                    v_data = v_data.get(field, None)
                    if not v_data:
                        break
                else:
                    v_data = None
                    break
        return v_data

    def get(self, item):
        if not isinstance(self.data, dict):
            raise ValueError(f"{self.data} is not dict!")
        if ":" in item:
            value = self.depth_handle(self.data, item.split(":"))
        else:
            value = self.depth_handle(self.data, [item])
        return value

    def parse(self, ignore_key_none=True, ignore_none=True):
        if self.iter_status:
            return [type(self)(data).add_mappings(self.item_mappings).add_callback(self.callbacks, self.parser).parse(
                ignore_key_none, ignore_none) for data in self.iter_data if data]
        return self.parse_dict(ignore_key_none, ignore_none)

    def parse_dict(self, ignore_key_none=True, ignore_none=True):
        mappings = {}
        for key, value in self.item_mappings.items():
            key = self.parse_key(key)
            if ignore_key_none and key is None:
                continue
            value = self.parse_value(value)
            if ignore_none and not all([key is not None, value is not None]):
                continue
            mappings[key] = value
        for callbacks in self.callbacks:
            for k, frm in callbacks.items():
                mappings[k] = frm(mappings) if callable(frm) else frm
        if self.parser:
            assert issubclass(self.parser, Parse), "解释类不在允许范围内, 请继承Parse!"
            mappings = self.parser(mappings).parse()
        return mappings

    def parse_key(self, key):
        return self[key[1:]] if key[0] == "!" else key

    def parse_value(self, values):
        return self[values[1:]] if values[0] == "!" else values


if __name__ == '__main__':
    x = {"a": 1, "b": 2, "c": {"d": 4}}
    mp = {"!a": "!c:d"}  # {1: 4}
    print(ParseDict(x).add_mappings(mp).parse())

    x = {"1": {"a": 1}, "2": {"a": 2}}
    mp = {"a": "!*:b|a"}  # {'a': {'b': 2}}
    print(ParseDict(x).add_mappings(mp).parse())

    x = {"1": {"a": 1}, "2": {"a": 2}}
    mp = {"a": "!*:a"}  # {'a': [1, 2]}
    print(ParseDict(x).add_mappings(mp).parse())

    x = {"1": {"a": 1}, "2": {"a": 2}}
    mp = {"a": "!*@:a"}  # {'a': [1, 2]}
    print(ParseDict(x).add_mappings(mp).parse())

    x = {"1": {"a": 1}, "2": {"a": 2}}
    mp = {"a": "!*:b|a"}  # {'a': {'b': 2}}  # 只取最后一个
    print(ParseDict(x).add_mappings(mp).parse())

    x = {"1": {"a": 1}, "2": {"a": 2}}
    mp = {"a": "!*@:b|a"}  # {'a': [{'b': 1}, {'b': 2}]}
    print(ParseDict(x).add_mappings(mp).parse())

    x = {"1": [{"b": 1}], "2": [{"b": 2}], 3: [{"e": 4}]}
    mp = {"a": "!*:@:b"}  # {'a': [1, 2]}
    print(ParseDict(x).add_mappings(mp).parse())

    x = {"1": [{"b": 1}], "2": [{"b": 2}], 3: [{"e": 4}]}
    mp = {"a": "!*:@:e|b"}  # {'a': [{'e': 1}, {'e': 2}, {'e': None}]}
    print(ParseDict(x).add_mappings(mp).parse())

    x = {"a": {"b": {"c": 1}}}
    mp = {"a": "!a:b:c"}  # {'a': 1}
    print(ParseDict(x).add_mappings(mp).parse())

    x = {"a": {"b": 1, "c": 2}}
    mp = {"a": "!a:e|b,d|f"}  # {'a': {'e': 1, 'd': None}}
    print(ParseDict(x).add_mappings(mp).parse())

    x = {"a": [{"b": 1}, {"b": 3}]}
    mp = {"a": "!a:@:b"}
    print(ParseDict(x).add_mappings(mp).parse())

    x = {"a": {"b": [{"e": 2}], "c": 1}}
    mp = {"a": "!a:*:@:e"}
    print(ParseDict(x).add_mappings(mp).parse())

    x = Data.load("../cloud/fixtures/huawei_describe_instance.json")
    mp = Data.load("../cloud/cloud_sdk/huawei/mappings/describe_instances.json")
    print(ParseDict(x.get("server", {})).add_mappings(mp).parse())
