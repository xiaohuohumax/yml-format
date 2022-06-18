from ruamel.yaml import CommentedMap

from format_model import FormatModel


class FormatModelItem(FormatModel):
    from_path: str = "./example/application.yml"
    target_path: str = "./example/application.yml"
    describe: str = "测试 List 类型"

    def format_data(self, root: CommentedMap):
        # 修改List
        root['hobby'] = ["games", "fish"]
        # 添加注释
        root.yaml_add_eol_comment("user name", 'username')
        pass
