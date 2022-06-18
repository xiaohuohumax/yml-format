from ruamel.yaml import CommentedMap

from format_model import FormatModel


class FormatModelItem(FormatModel):
    from_path: str = "./application-db.yml"
    target_path: str = "./application-db.yml"
    describe: str = "格式化 application-db.yml"

    def format_data(self, root: CommentedMap):
        # 更改配置 子类覆盖重写
        datasource = root['spring']['datasource']
        datasource['username'] = 'dev-username'
        datasource['password'] = 'dev-password'
        pass
