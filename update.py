# coding=utf-8

import os
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
        self.passwords = set()

    def get_all_passwords(self) -> list:
        """
        获取数据
        """
        count = self.collection.count()
        i = 1
        while True:
            s = self.collection.find({}).skip(1000*i).limit(1000)
            for item in s:
                self.passwords.add(item["p"])
            print(f"{len(self.passwords)}/{count}")
            if s.count() < 1000:
                break
            i += 1
        return self.passwords

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
    export.get_all_passwords()
    export.close()


if __name__ == '__main__':
    main()
