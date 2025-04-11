
import os
class TemplateParser():
    
    
    def __init__(self, language: str = None, defualt_lang = "en"):
        self.current_path =  os.path.dirname(os.path.abspath(__file__))
        self.default_lang = defualt_lang
        self.language =  None
        self.set_lang(language= language)
    
    def set_lang(self, language: str):
        
        language_path  = os.path.join(self.current_path, "Locales", language)
        if language or os.path.exists(language_path):
            self.language = language
        
        self.language = self.default_lang
        
    def get(self, group: str, key: str, vars: dict = {}):
        if not group or not key:
            return None
        
        group_path = os.path.join(self.current_path, "Locales", self.language, f"{group}.py")
        target_lang =  self.language
        
        if not os.path.exists(group_path):
            group_path = os.path.join(self.current_path, "Locales", self.default_lang, f"{group}.py")
            target_lang = self.default_lang
            
        if not os.path.exists(group_path):
            return None
        
        #importing group module
        module = __import__(f"stores.llm.PromptTemplates.Locales.{target_lang}.{group}", fromlist=[group])
        
        if not module:
            return None
        
        key_attribute = getattr(module, key)
        return key_attribute.substitute(vars) 