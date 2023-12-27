from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("re_data"),
    autoescape=select_autoescape()
)

def render_dbt_project(project_name):
    template = env.get_template("dbt_project.yml")
    return template.render(project_name=project_name)

def render_email_alert(alerts, owner, models_to_notify):
    template = env.get_template("email_alert.html")
    return template.render(alerts=alerts, owner=owner, models_to_notify=models_to_notify)