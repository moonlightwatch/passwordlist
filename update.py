# coding=utf-8

import os
import re
import json
import pymongo


class ExportPasswordList(object):
    """
    导出密码字典
    """

    def __init__(self):
        self._config = self._get_config()
        self._db_client = self._get_db(self._config)
        self.collection = self._get_dbcollection(self._config)
        self.passwords = list()

        self._numbers = list()
        self._letters = list()
        self._letters_upper = list()
        self._letter_lower = list()
        self._num_letters = list()
        self._num_symbols = list()
        self._letter_symbols = list()
        self._num_letter_symbols = list()

    def output(self) -> None:
        """
        输出成文件
        """
        with open(file="passwords.txt", mode="w") as fp:
            for item in self.passwords:
                fp.write(item)
                fp.write("\n")
        with open(file="num_letter_symbols.txt", mode="w") as fp:
            for item in self._num_letter_symbols:
                fp.write(item)
                fp.write("\n")
        with open(file="letter_symbols.txt", mode="w") as fp:
            for item in self._letter_symbols:
                fp.write(item)
                fp.write("\n")
        with open(file="num_symbols.txt", mode="w") as fp:
            for item in self._num_symbols:
                fp.write(item)
                fp.write("\n")
        with open(file="num_letters.txt", mode="w") as fp:
            for item in self._num_letters:
                fp.write(item)
                fp.write("\n")
        with open(file="letter_lower.txt", mode="w") as fp:
            for item in self._letter_lower:
                fp.write(item)
                fp.write("\n")
        with open(file="numbers.txt", mode="w") as fp:
            for item in self._numbers:
                fp.write(item)
                fp.write("\n")
        with open(file="letters.txt", mode="w") as fp:
            for item in self._letters:
                fp.write(item)
                fp.write("\n")
        with open(file="letters_upper.txt", mode="w") as fp:
            for item in self._letters_upper:
                fp.write(item)
                fp.write("\n")

    def push(self) -> None:
        """
        推送
        """
        os.popen(cmd="git add .").read()
        os.popen(cmd="git commit -m \"update\"").read()
        os.popen(cmd="git push").read()

    def load_all_passwords(self) -> None:
        """
        获取数据
        """
        count = self.collection.count()
        i = 1
        while True:
            s = self.collection.find({}).skip(1000*i).limit(1000)
            pwd_list = list()
            for item in s:
                self.passwords.append(item["p"])
                pwd_list.append(item["p"])
            print(f"{len(self.passwords)}/{count}")
            self._check_passwords(pwd_list)
            if len(self.passwords) > count:
                break
            i += 1

    def _check_passwords(self, passwords: list) -> None:
        """
        分类
        """
        for pwd in passwords:
            if re.match("^\d+$", pwd):
                self._numbers.append(pwd)
            elif re.match("^[A-Za-z]+$", pwd):
                self._letters.append(pwd)
                if re.match("^[A-Z]+$", pwd):
                    self._letters_upper.append(pwd)
                elif re.match("^[a-z]+$", pwd):
                    self._letter_lower.append(pwd)
            elif re.match("^[A-Za-z0-9]+$", pwd) and re.search("[A-Za-z]+", pwd) != None and re.search("[0-9]+", pwd) != None:
                self._num_letters.append(pwd)
            else:
                if re.search("[0-9]+", pwd) == None:
                    self._letter_symbols.append(pwd)
                elif re.search("[A-Za-z]+", pwd) == None:
                    self._num_symbols.append(pwd)
                else:
                    self._num_letter_symbols.append(pwd)

    def _get_config(self) -> dict:
        """
        从配置文件获取配置
        """
        json_str = ""
        with open(file="config.json", mode="r", encoding="utf-8") as fp:
            json_str = fp.read()
        return json.loads(s=json_str)

    def _get_db(self, config: dict) -> pymongo.mongo_client.MongoClient:
        """
        获取数据库客户端实例
        """
        return pymongo.mongo_client.MongoClient(
            host=config["host"], port=config["port"])

    def _get_dbcollection(self, config: dict) -> pymongo.collection.Collection:
        """
        获取数据库Collection
        """
        up = self._db_client.get_database(config["db"])
        up.authenticate(name=config["user"], password=config["pwd"])
        return up.get_collection("p")

    def close(self):
        """
        关闭数据库链接
        """
        self._db_client.close()


def main():
    export = ExportPasswordList()
    export.load_all_passwords()
    export.output()
    export.push()
    export.close()


if __name__ == '__main__':
    main()
