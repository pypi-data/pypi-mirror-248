import importlib
import os
import finhack.library.log as Log
class ClassLoader():
    def get_module(module_path='',user_module_path=''):
        if os.path.exists(user_module_path):
            filename = os.path.basename(user_module_path)
            module_name = "user_module"
            if filename.endswith(".py"):
                module_name = filename[:-3]
            module_spec = importlib.util.spec_from_file_location(module_name, user_module_path)
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
        elif not os.path.exists(user_module_path):
            try:
                module=importlib.import_module(module_path)
            except ModuleNotFoundError:
                Log.logger.warning(f"Module '{module_path}' does not exist，use base_loader")
                module=importlib.import_module('finhack.core.loader.base_loader')
                
        else:
            Log.logger.critical("module_path:"+module_path+",user_module_path:"+user_module_path+"均不存在！")
            exit()
            
        return module
    
    def get_object(class_name):
        pass