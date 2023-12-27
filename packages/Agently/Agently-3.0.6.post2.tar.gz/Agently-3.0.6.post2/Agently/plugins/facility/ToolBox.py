from .utils import FacilityABC
from Agently.utils import RuntimeCtx, RuntimeCtxNamespace

class ToolBox(FacilityABC):
    def __init__(self, *, storage: object, plugin_manager: object, settings: object):
        self.tools = RuntimeCtx()
        self.categories = RuntimeCtx()

    def register_tool(self, name: str, desc: any, args: dict, func: callable, *, categories: (str, list)=["$global"]):
        tool = RuntimeCtxNamespace(name, self.tools)
        tool.update({
            "desc": desc,
            "args": args,
            "func": func
        })
        if isinstance(categories, str):
            categories = [categories]
        for category in categories:
            if self.categories.get(category):
                tool_list = self.categories.get(f"{ category }.list", [])
                if name not in tool_list:
                    tool_list.append(name)
                    self.categories.set(f"{ category }.list", tool_list)
        return self

    def update_tool(self, name: str, key: str, value: any):
        tool = RuntimeCtxNamespace(name, self.tools)
        tool.update(key, value)
        return self

    def update_category(self, category_name: str, category_desc: any):
        self.categories.update(f"{ category_name }.desc", category_desc)
        return self

    def get_tool_info(self, tool_name: str, *, with_args: bool=False):
        tool = self.tools.get(tool_name)
        if tool and "desc" in tool:
            if with_args:
                return {
                    "name": tool_name,
                    "desc": tool["desc"],
                    "args": tool["args"] if "args" in tool else {}
                }
            else:
                return {
                    "name": tool_name,
                    "desc": tool["desc"],
                }
        else:
            return None

    def get_tool_list(self, *, with_args: bool=False, categories: (str, list)=["$global"]):
        result = []
        if isinstance(categories, str):
            categories = [categories]
        for category in categories:
            if category in self.categories:
                for tool_name in self.categories[category]:
                    tool_info = self.get_tool_info(tool_name, with_args = with_args)
                    result.append(tool_info)
        return result

    def get_tool_func(self, tool_name: str):
        return self.tools.get(f"{ tool_name }.func")

    def call_tool_func(self, tool_name: str, args: dict):
        func = self.get_tool_func(tool_name)
        if func:
            return func(**args)
        else:
            return { "no_func": True }

def export():
    return ("tool_box", ToolBox)