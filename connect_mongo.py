from mongoengine import connect
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

mongo_user = config.get("DB", "user")
mongodb_pass = config.get("DB", "pass")
app_name = config.get("DB", "app_name")
domain = config.get("DB", "domain")

connect(
    host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/?retryWrites=true&w=majority&appName={app_name}""",
    ssl=True,
)
