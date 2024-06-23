from jinja2 import Environment, FileSystemLoader


file_loader = FileSystemLoader("server/templates")

env = Environment(loader=file_loader)


def genearte_prompt(template_file: str, data: dict):
    template = env.get_template(template_file)
    return template.render(data)


if __name__ == "__main__":
    data = {"user_input": "测试一下"}
    # data = {"data": "测试一下"}
    print(genearte_prompt("input_rail.tpl", data))
