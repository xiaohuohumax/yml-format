from ruamel.yaml import CommentedMap

from format_model import FormatModel


class FormatModelItem(FormatModel):
    """
    模块范例
    注意: 必须继承 FormatModel 且 类名固定为 FormatModelItem
    """
    # 是否使用相对路径模式
    # True: from_path,target_path 相对于基础路径
    # False: from_path,target_path 为绝对路径
    relative_path_model: bool = True
    # 模块名称 空时默认为包路径
    model_name: str = ""
    # 源文件相对/绝对路径
    from_path: str = "./application-db.yml"
    # 目标文件相对/绝对路径
    target_path: str = "./docker-stack.yml"
    # 是否禁用此模块
    disabled: bool = True
    # 模块描述
    describe: str = "格式化 docker-stack.yml"

    def format_data(self, root: CommentedMap):
        # 更改配置 子类覆盖重写
        pass
