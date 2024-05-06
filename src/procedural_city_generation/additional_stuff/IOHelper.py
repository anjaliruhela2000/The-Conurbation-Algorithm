

class StdoutRedirector(object):
    def __init__(self, label_obj,pyQt_app=None):
        self.label_obj=label_obj
        self.pyQt_app=pyQt_app

    def write(self, out):
        self.label_obj.insertPlainText(out)
        self.pyQt_app.processEvents()
