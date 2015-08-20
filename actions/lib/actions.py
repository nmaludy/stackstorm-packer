from st2actions.runners.pythonrunner import Action
import packer
import os


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self.atlas_token = self.config.get('atlas_token', None)
        self._exec_path = self.config.get('exec_path', '/usr/local/bin/packer')
        self._global_vars = self.config.get('variables', None)

    def _get_vars(self, variables):
        if self._global_vars and variables:
            return self._mergedicts(self._global_vars, variables)
        if self._global_vars and not variables:
            return self._global_vars
        else:
            return variables

    def _mergedicts(dict1, dict2):
        merged_dict = dict1.copy()
        merged_dict.update(dict2)
        return merged_dict

    def set_dir(self, directory):
        os.chdir(directory)

    def packer(self, packerfile, exc=None, only=None, vars=None, vars_file=None):
        # Cast as string from unicode to appease upstream module
        _packerfile = str(packerfile)
        return packer.Packer(_packerfile, exc=exc, only=only,
                             vars=self._get_vars(vars), vars_file=vars_file,
                             exec_path=self._exec_path)
