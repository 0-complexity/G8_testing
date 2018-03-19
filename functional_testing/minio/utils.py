import os, uuid, time

class Utils:

    def random_string(self, length=10):
        return str(uuid.uuid4()).replace('-', '')[:length]

    def create_file(self, path='/tmp'):
        file_name = self.random_string()
        file_data = self.random_string()
        file_path = os.path.join(path, file_name)
        os.system('echo "%s" > %s' % (file_data, file_path))
        return file_path, file_data

    def delete_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    def read_file(self, file_path):
        with open(file_path, 'r') as f:
            data = f.read()
        return data

    def random_prefix(self, levels=2):
        prefix = ''
        for _ in range(levels):
            level_name = self.random_string()
            prefix = os.path.join(prefix, level_name)
        
        return prefix
