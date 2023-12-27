import peewee


def patch_models(module):
    from lemon_rag.lemon_models import models
    for attr_name in dir(models):

        attr = getattr(models, attr_name)
        # print(type(attr))
        if not isinstance(attr, type):
            continue
        if not issubclass(attr, peewee.Model):
            continue
        setattr(models, attr_name, module.get(attr_name))
