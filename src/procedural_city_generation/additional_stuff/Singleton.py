class Singleton:

    class __Singleton:
        def __init__(self, modulename=None):
            import procedural_city_generation
            import os
            import json
            if modulename:
                path=os.path.dirname(procedural_city_generation.__file__)
                with open(path+"/inputs/"+modulename+".conf", 'r') as f:
                    d=json.loads(f.read())
                for k, v in d.items():
                    setattr(self, k, v["value"])
            else:
                print( "Warning, Singleton instanciated without parsing a json file. Please specify the modulename parameter to avoid errors")
    instance=None
    def __init__(self, modulename=None):
        
        if not Singleton.instance:
            Singleton.instance=Singleton.__Singleton(modulename)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        setattr(self.instance, name, value)

    def kill(self):
        Singleton.instance = None
