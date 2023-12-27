import psutil


class ExecutableRunning:
    executable: str | None

    def __init__(self, args):
        if args.screensaver_executable:
            self.executable = args.screensaver_executable
        else:
            self.executable = None
    
    def name(self):
        if self.executable:
            return f"Inactive if executable \"{self.executable}\" is running" 
        else:
            return "Whether a particular executable is running"
    
    def detection_problems(self):
        if not self.executable:
            return "No --screensaver-executable option given"
        return None
    
    def is_active(self):
        if not self.executable:
            raise RuntimeError('Need an executable')
        for proc in psutil.process_iter():
            cmdline = proc.cmdline()
            if len(cmdline) == 0:
                continue
            executable = cmdline[0]
            if executable.find(self.executable) != -1:
                return False
        return True
