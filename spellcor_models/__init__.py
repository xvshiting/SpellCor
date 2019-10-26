import importlib
import os

registered_language_models = {}


def register_lang_model(name):
    def inner(obj):
        def most_inner():
            registered_language_models[name] = obj
        most_inner()
        return obj
    return inner


# automatically import any Python files in the models/ directory
for file in os.listdir(os.path.dirname(__file__)):
    if file.endswith('.py') and not file.startswith('_'):
        model_name = file[:file.find('.py')]
        module = importlib.import_module('spellcor_models.' + model_name)
