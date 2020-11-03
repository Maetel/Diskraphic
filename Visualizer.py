from abc import ABC, abstractmethod
import numpy as np
import math

_clamp = lambda x, l, u: l if x < l else u if x > u else x

class IVisualizer(ABC):
    @abstractmethod
    def update(self, file_info):
        pass
    @abstractmethod
    def visualize(self, width=500, height=500):
        pass

def extension(path):
    begin = path.find('.')
    return False if begin == -1 else path[begin+1:-1].lower()

class Simplest(IVisualizer):
    MAX_SIZE = 1000 # for test purpose
    elem_idx = 0
    infos = []
    extensions = []
    index_by_size = []
    total_size = 0
    size_min, size_max = -1, -1
    last_img = None

    def __init__(self):
        #reserve memory
        self.infos = [None] * self.MAX_SIZE

    def update(self, file_info):
        if not file_info or (self.elem_idx >= self.MAX_SIZE):
            return False
        self.infos[self.elem_idx] = file_info
        self.elem_idx += 1
        return True
        
    def visualize(self, width=500, height=500):
        return self.infos[:self.elem_idx]
    
    def last_result(self):
        return None

class Graphwise(IVisualizer):
    MAX_SIZE = 1000 # for test purpose
    elem_idx = 0
    infos = []
    extensions = []
    index_by_size = []
    total_size, total_name_len, total_path_len = 0, 0, 0
    size_min, size_max = -1, -1
    name_len_min, name_len_max = -1, -1
    path_len_min, path_len_max = -1, -1
    last_img = None

    def __init__(self):
        #reserve memory
        self.infos = [None] * self.MAX_SIZE

    def _update_name(self, name):
        val = len(name)
        self.total_name_len += val
        self.avg_name_len = self.total_name_len/self.last_idx
        self.name_len_min = val if (self.name_len_min == -1) or (self.name_len_min > val) else self.name_len_min
        self.name_len_max = val if (self.name_len_max == -1) or (self.name_len_max < val) else self.name_len_max

    def _update_path(self, path):
        val = len(path)
        self.total_path_len += val
        self.avg_path_len = self.total_path_len/self.last_idx
        self.path_len_min = val if (self.path_len_min == -1) or (self.path_len_min > val) else self.path_len_min
        self.path_len_max = val if (self.path_len_max == -1) or (self.path_len_max < val) else self.path_len_max
        

    def _update_size(self, size):
        self.total_size += size
        self.avg_size = self.total_size/self.last_idx
        self.size_min = size if (self.size_min == -1) or (self.size_min > size) else self.size_min
        self.size_max = size if (self.size_max == -1) or (self.size_max < size) else self.size_max

    def update(self, file_info):
        if not file_info or (self.elem_idx >= self.MAX_SIZE):
            return False
        self.infos[self.elem_idx] = file_info
        ext = extension(file_info.name)
        if ext not in self.extensions:
            self.extensions.append(ext)
        self.elem_idx += 1
        self.last_idx = file_info.index
        self.total_dirs = file_info.total_dirs
        self._update_size(file_info.size)
        self._update_name(file_info.name)
        self._update_path(file_info.path)
        return True
    
    def stat(self):
        return (self.elem_idx, self.total_dirs, self.size_max, self.total_size)

    def visualize(self, width=500, height=500, grayscale=False):
        #retval = np.zeros((height, width, 1), dtype=np.uint8)
        avg_intensity = _clamp(int(255 * (self.avg_size/self.size_max)), 0, 255)
        if grayscale:
            avg_intensity = 255 - avg_intensity
        avg_name_len = int(255 * (self.avg_name_len/self.name_len_max))
        avg_path_len = int(255 * (self.avg_path_len/self.path_len_max))
        retval = None
        if grayscale:
            retval = np.full((height, width, 1), avg_intensity, dtype=np.uint8)
        else: #rgb
            retval = np.full((height, width, 3), (avg_intensity, avg_name_len, avg_path_len),dtype=np.uint8)
        valid_infos = self.infos[:self.elem_idx]
        #valid_infos.sort(key=lambda info: info.size) #this might take tons of time
        col_wid = width / (self.elem_idx)
        row_hi = height / (self.elem_idx)
        
        #colwise
        if not False:
            row_offset = 0.1
            for col, info in enumerate(valid_infos):
                ratio = math.sqrt(info.size/ self.size_max)
                ratio = _clamp(ratio, 0, 1-row_offset)
                mid_row = int(height/2)
                row = int(_clamp(int(height * ratio), 0, height-1)/2)
                col_begin = int(col_wid * col)
                col_end = int(col_wid * (col+1))

                if grayscale:
                    intensity = int(255 * ratio)
                    retval[mid_row - row : mid_row + row, col_begin:col_end] = 255 - intensity
                else:
                    name_ratio = len(info.name) / self.name_len_max
                    path_ratio = len(info.path) / self.path_len_max
                    #name_ratio = math.sqrt(name_ratio)
                    #path_ratio = math.sqrt(path_ratio)
                    size_dependency = 255
                    name_dependency = 255
                    path_dependency = 255
                    #size_dependency + name_dependency + path_dependency
                    _r = int(size_dependency * ratio + 255 - size_dependency)
                    _g = int(name_dependency * name_ratio + 255 - name_dependency)
                    _b = int(path_dependency * path_ratio + 255 - path_dependency)
                    retval[mid_row - row : mid_row + row, col_begin:col_end] = (_r, _g, _b)

        #rowwise
        if False:
            for row, info in enumerate(valid_infos):
                ratio = info.size/self.size_max
                col = _clamp(int(width * ratio), 0, width-1)
                #col_begin = _clamp(int(col_wid * col), 0, width)
                #col_end = _clamp(int(col_wid * (col+1)), 0, width)
                row_begin = int(row_hi * row)
                row_end = int(row_hi * (row+1))
                intensity = 255 - int(255 * ratio)
                #if not np.sum(retval[row_begin:row_end, 0:width-1]):
                retval[row_begin:row_end, 0:width-1] = 255-intensity
                retval[height - 1 - row_end : height - 1 - row_begin, width-1 - col : width-1] = intensity
        self.last_img = retval[:]
        return retval
    
    def last_result(self):
        return self.last_img[:]

if __name__ == "__main__":
    vis = Simplest()
    vis.visualize()