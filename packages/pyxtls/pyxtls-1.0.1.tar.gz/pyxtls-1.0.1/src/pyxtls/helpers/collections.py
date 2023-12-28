# -*- coding: utf-8 -*-
# author: HPCM
# time: 2023/12/21 15:38
# file: 20-test.py
import re


class Node(object):

    def __init__(self, name, rate, prev_value, value=0):
        self.name = name
        self.rate = rate
        self.prev = prev_value
        self.next = None
        self._value = value

    def format_value(self):
        if not self.rate:
            return
        while self._value < 0 and self.next:
            self._value += self.rate
            self.next.value -= 1
        while self._value > self.rate and self.next:
            self._value -= self.rate
            self.next.value += 1

        # print(isinstance(self._value, float), self._value % 1, self.prev, self.name)
        if isinstance(self._value, float) and self._value % 1 and self.prev:
            self.prev.value += self.next.rate * self._value % 1
            self._value = self._value // 1
        return int(self._value)

    @property
    def value(self):
        self.format_value()
        return self._value

    @value.setter
    def value(self, v):
        self._value = v
        self.format_value()

    def __sub__(self, other):
        if not isinstance(other, type(self)) and self.name != other.name:
            raise ValueError("不支持!")

        return type(self)(self.name, self.rate, self.prev, self.value - other.value)

    def __add__(self, other):
        if not isinstance(other, type(self)) and self.name != other.name:
            raise ValueError("不支持!")

        return type(self)(self.name, self.rate, self.prev, self.value + other.value)

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.value} {self.name}>"


class Convert(object):
    converts = []

    def __init__(self, s):
        self.data = None
        self.convert_update(s)
        self.convert_data()

    def convert_update(self, s):
        for i, v in enumerate(self.converts):
            res = re.findall(r"(\d+?) *%s" % v["name"], s, flags=re.S)
            if not res:
                continue
            if len(res) != 1:
                raise ValueError(f"{v['name']} 存在重复!")
            self.converts[i].update(value=int(res[0]))

    def convert_data(self):
        prev_value = None

        for cm in self.converts[::-1]:
            value = Node(cm["name"], cm["rate"], prev_value, cm.get("value", 0))
            value.prev = prev_value
            if prev_value is None:
                self.data = value
            else:
                prev_value.next = value

            prev_value = value

    def __sub__(self, other):
        if not isinstance(other, type(self)):
            raise ValueError("不支持!")
        s_data, o_data = self.data, other.data
        while True:
            while s_data.name == o_data.name:
                s_data.value -= o_data.value
                if s_data.next:
                    s_data = s_data.next
                else:
                    break
            if not o_data.next:
                break
            o_data = o_data.next
        return self

    def __add__(self, other):
        if not isinstance(other, type(self)):
            raise ValueError("不支持!")
        s_data, o_data = self.data, other.data
        while True:
            while s_data.name == o_data.name:
                s_data.value += o_data.value
                if s_data.next:
                    s_data = s_data.next
                else:
                    break
            if not o_data.next:
                break
            o_data = o_data.next
        return self

    def __str__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.get_format())

    def __float__(self):
        return self.get_value()

    def get_value(self, rate_str=None):
        if not self.data:
            return float(0)
        data = self.data

        value = 0
        use_rate = 0
        prev_rate = 1
        while True:
            value += data.value * prev_rate
            if not data.next:
                break
            if rate_str and data.name == rate_str:
                use_rate = prev_rate
            prev_rate *= data.rate
            data = data.next
        return value / (use_rate or prev_rate)

    def get_format(self):
        if not self.data:
            return str(None)
        data = self.data

        value = ""
        while True:
            value = f" {data.value} {data.name}" + value
            if not data.next:
                break

            data = data.next
        return value


if __name__ == '__main__':
    class WenDaoConvert(Convert):
        converts = [
            {"name": "年", "rate": None},
            {"name": "天", "rate": 365},
            {"name": "点", "rate": 1440}
        ]


    a = WenDaoConvert("123年4444天1点")
    b = WenDaoConvert("0年43天1444点")
    print(a + b)
    print(a - b)
