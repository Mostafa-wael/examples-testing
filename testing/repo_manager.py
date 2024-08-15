import os
import subprocess
from testing.logger import Logger

class RepoManager:
    ''' Singleton class to manage the repos '''
    _instance = None

    def __init__(self, repo_url):
        if RepoManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            RepoManager._instance = self
            self.repo_url = repo_url
            self.logger = Logger.get_instance()

    @staticmethod
    def get_instance():
        ''' Static access method for singleton '''
        if RepoManager._instance is None:
            RepoManager(None)
        return RepoManager._instance
    
    def clone_repo_if_not_exist(self):
        ''' Clone the repo if not already cloned '''
        try:
            repo_name = self.repo_url.split('/')[-1].split('.')[0]
            if os.path.isdir(repo_name):
                self.logger.warning("Repo is already cloned!")
            else:
                process = subprocess.Popen(['git', 'clone', self.repo_url], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                _, stderr = process.communicate()
                stderr = stderr.decode('utf-8')
                error_keywords = ["Fatal", "fatal", "error", "Error", "ERROR"]
                if any(keyword in stderr for keyword in error_keywords):
                    raise ValueError(stderr)
                self.logger.debug("Repo is cloned successfully!")
        except ValueError as e:
            self.logger.error(f"Error: {e}")
            raise ValueError(f"Error: {e}")
