import os, uuid, time, hashlib

class Utils:

    def get_file_md5(self, file_path):
        filehash = hashlib.md5()
        filehash.update(open(file_path).read().encode('utf-8'))
        return filehash.hexdigest()

    def random_string(self, length=10):
        return str(uuid.uuid4()).replace('-', '')[:length]

    def create_object(self, path='/tmp'):
        file_prefix = self.random_prefix()
        file_name = self.random_string()
        file_data = self.random_string()
        file_path = os.path.join(path, file_name)
        os.system('printf "%s" > %s' % (file_data, file_path))
        file_obj = {
            'name':file_name,
            'prefix':file_prefix,
            'path':file_path,
            'data':file_data,
            'decr':open(file_path, 'rb'),
            'stat':os.stat(file_path),
            'md5':self.get_file_md5(file_path)
        }
        
        return file_obj

    def delete_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    def read_file(self, file_path):
        with open(file_path, 'r') as f:
            data = f.read()
        return data

    def random_prefix(self, levels=3):
        prefix = ''
        for _ in range(levels):
            level_name = self.random_string()
            prefix = os.path.join(prefix, level_name)
        
        return prefix
