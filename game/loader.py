import inspect
import importlib
import regex
import os

from django.template.loaders.filesystem import Loader as FilesystemLoader

from game.exceptions import UnexpectedState

ruleset = None
gamedata = None

###
# Custom template loader to be used for gamedata templates. 
#
class GamedataTemplateLoader(FilesystemLoader):
    def get_template_sources(self, template_name, template_dirs=None): 
        if (gamedata):
            module_dir = os.path.dirname(os.path.abspath(gamedata.__file__))
            yield os.path.join(os.path.join(module_dir, 'templates'), template_name) 
            

    

##
# Loads all gamedata available in the given module
#
def load_gamedata(mod):
    global gamedata, ruleset

    if (not gamedata is None):
        return
    
    gamedata = importlib.import_module(mod)
    ruleset = gamedata.get_ruleset()
   
def get_ruleset():
    global ruleset

    assert(gamedata)

    return ruleset
