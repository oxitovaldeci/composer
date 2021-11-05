from django.apps import AppConfig


def createAppConfig(name):
    type(
        name + "Config",
        (AppConfig,),
        dict(
            default_auto_field='django.db.models.BigAutoField',
            name=name.lower()
        )
    )


createAppConfig("Search")
createAppConfig("Accounts")
createAppConfig("Home")
