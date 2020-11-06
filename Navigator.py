import os
from collections import deque

class FileInfo:
    def __init__(self, name, path, index, total_dirs):
        self.name = name
        self.path = path
        self.full_path = f"{path}/{name}"
        self.size = os.stat(self.full_path).st_size
        self.index = index
        self.total_dirs = total_dirs
        #self.dir_depth = dir_depth
    

class Navigator:
    _depth_counter = ":__depth_counter__:"
    def clear(self):
        self.dir_depth = 0
        self.total_dirs = 0 #including root
        self.index = 1 # 1-based index
        self.dirs = deque()
        self.files = deque()

    def set_path(self, dir = ""):
        self.clear()
        if not dir:
            dir = os.getcwdb().decode('utf-8')
            print(f"Navigator - Not a directory. Setting root directory to '{dir}'")
        if not dir.endswith('/'):
            dir = dir + '/'
        if os.path.isdir(dir) and (not dir in self.dirs):
            self.dirs.append(dir)
            self.dirs.append(self._depth_counter)

    def __init__(self, dir=""):
        self.set_path(dir)

    def read_next(self):
        if self.files:
            info = FileInfo(self.files[0], self.last_dir, self.index, self.total_dirs)
            self.index += 1
            self.files.popleft()
            return info
        if self.dirs and self.dirs[0] == self._depth_counter:
            self.dir_depth += 1
            self.dirs.popleft()
            while self.dirs and self.dirs[0] == self._depth_counter:
                self.dir_depth -= 1
                self.dirs.popleft()
        if self.dirs:        
            self.last_dir = self.dirs[0]
            self.dirs.popleft()
            self.total_dirs+=1
            for path in os.listdir(self.last_dir):
                abs_path = f"{self.last_dir}/{path}"
                if os.path.isfile(abs_path):
                    self.files.append(path) #handover relative file name
                else:
                    self.dirs.append(abs_path)
            self.dirs.append(self._depth_counter)
            return self.read_next()
        return None

if __name__ == "__main__":
    stat = os.stat('Navigator.py')
    print("Whole stat : ", stat)
    print("Size : ", stat.st_size)
    print("DIr : ", os.listdir())
    nav = Navigator()