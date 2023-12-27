import os

from ..file_importer import import_module_from_file

class CustomActiveDetector:
    def __init__(self, args):
        self.args = args
        custom_path = args.active_detector
        custom_expanded_path = os.path.expanduser(custom_path)
        if os.path.exists(custom_expanded_path):
            self.custom_module = import_module_from_file(
                'custom_idle_detector', custom_expanded_path)
        else:
            self.custom_module_problem =  "File not found: " + custom_path

    def name(self):
        return 'Custom detector'


    def detection_problems(self):
        if self.custom_module_problem:
            return self.custom_module_problem
        return self.custom_module.detection_problems(self.args)


    def is_active(self):
        return self.custom_module.is_active(self.args)