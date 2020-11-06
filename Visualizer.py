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
    def __init__(self):
        #declare
        self.MAX_SIZE = 1000 # for test purpose
        self.elem_idx = 0
        self.infos = []
        self.extensions = []
        self.index_by_size = []
        self.total_size = 0
        self.size_min, self.size_max = -1, -1
        self.last_img = None

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
    
    def __init__(self):
        #declare
        self.MAX_SIZE = 1000 # for test purpose
        self.elem_idx = 0
        self.infos = []
        self.extensions = []
        self.index_by_size = []
        self.total_size, self.total_name_len, self.total_path_len = 0, 0, 0
        self.size_min, self.size_max = -1, -1
        self.name_len_min, self.name_len_max = -1, -1
        self.path_len_min, self.path_len_max = -1, -1
        self.last_img = None
        self.total_dirs = None
        self.last_idx = None
        
        self.avg_size, self.avg_name_len, self.avg_path_len = None, None, None

        #reserve memory
        self.infos = [None] * self.MAX_SIZE

    #TODO : unify these
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

    def visualize(self, width=500, height=500, grayscale=False, DNA_ish=True):
        avg_intensity = _clamp(int(255 * (self.avg_size/self.size_max)), 0, 255)
        if grayscale:
            avg_intensity = 255 - avg_intensity
        avg_name_len = int(255 * (self.avg_name_len/self.name_len_max))
        avg_path_len = int(255 * (self.avg_path_len/self.path_len_max))
        rgb_background = (avg_intensity, avg_name_len, avg_path_len)
        retval = None
        if grayscale:
            retval = np.full((height, width, 1), avg_intensity, dtype=np.uint8)
        else: #rgb
            retval = np.full((height, width, 3), rgb_background,dtype=np.uint8)
        valid_infos = self.infos[:self.elem_idx]
        #valid_infos.sort(key=lambda info: info.size) #this might take tons of time
        col_wid = width / (self.elem_idx)
        row_hi = height / (self.elem_idx)
        
        #DNA-ish pitch and amplitude

        #colwise
        row_offset = 0.1

        #vars for DNA_ish
        DNA_amplitude = int(height * 0.3)
        DNA_pitch = 0.2 * DNA_amplitude
        shift_high = math.pi * 0.4
        shift_low = math.pi * 1.5
        def dna_y(dna_x):
            return height*0.5 +  DNA_amplitude * math.sin((math.pi*2/DNA_pitch) * dna_x + math.pi * shift_high)
        def draw_float_pt(x, y, val): #value can be either uint8_t or uint8_t[3]
            x_i, x_d = divmod(x, 1)
            y_i, y_d = divmod(y, 1)
            x_i, y_i = int(x_i), int(y_i)
            p11_w, p12_w, p21_w, p22_w = (1-x_d)*(1-y_d), (x_d)*(1-y_d), (1-x_d)*(y_d), (x_d)*(y_d)
            #interpolated = [[val * p11_w, val * p12_w], [val * p21_w, val * p22_w]]
            #retval[y_i:y_i+2, x_i:x_i+2] = interpolated #don't blend for now
            is_x_boundary = True if x_i >= width - 2 else False
            is_y_boundary = True if y_i >= height - 2 else False
            retval[y_i, x_i] = val*p11_w
            if not is_x_boundary:
                retval[y_i, x_i+1] = val*p12_w
            if not is_y_boundary:
                retval[y_i+1, x_i] = val*p21_w
            if not is_x_boundary and not is_y_boundary:
                retval[y_i+1, x_i+1] = val*p22_w
        def dna_row_begin_end(x):
            y = int(dna_y(x))
            grow_downwards = True if y < int(height*0.5) else False #upwards
            row_begin = y if grow_downwards else y - row
            row_end = y + row if grow_downwards else y
            return row_begin, row_end

        for col, info in enumerate(valid_infos):
            ratio = math.sqrt(math.sqrt(info.size/ self.size_max))
            #ratio = -math.log(info.size/ self.size_max, 2)
            ratio = _clamp(ratio, 0, 1-row_offset)
            mid_row = int(height/2)
            row = int(_clamp(int(height * ratio), 0, height-1)/2)

            row_begin = mid_row - row
            row_end = mid_row + row
            col_begin = int(col_wid * col)
            col_end = int(col_wid * (col+1))
            if DNA_ish:
                row_begin, row_end = dna_row_begin_end(col)

            if grayscale:
                if DNA_ish:
                    DNA_thickness = int(height * 0.03)
                    y = int(dna_y(col))
                    DNA_color = 255 - avg_intensity
                    sub_dna_ratio = 0.5
                    sub_DNA_color = int(255 * sub_dna_ratio + (1 - ratio) * DNA_color)
                    #sub dna
                    retval[height - (y+DNA_thickness+1):height - (y-DNA_thickness), col_begin:col_end] = sub_DNA_color
                    #main dna
                    retval[y-DNA_thickness:y+DNA_thickness+1, col_begin:col_end] = DNA_color
                intensity = int(255 * ratio)
                retval[row_begin:row_end, col_begin:col_end] = 255 - intensity
                

            else: #rgb
                if DNA_ish:
                    y = int(dna_y(col))
                    DNA_thickness = int(height *0.03)
                    DNA_color = (255 - rgb_background[0], 255 - rgb_background[1], 255 - rgb_background[2])
                    sub_dna_ratio = 0.5
                    def sub_dna_color():
                        r = height * sub_dna_ratio + (1 - sub_dna_ratio) * DNA_color[0]
                        g = height * sub_dna_ratio + (1 - sub_dna_ratio) * DNA_color[1]
                        b = height * sub_dna_ratio + (1 - sub_dna_ratio) * DNA_color[2]
                        return (r,g,b)

                    #sub dna
                    retval[height - (y+DNA_thickness+1):height - (y-DNA_thickness), col_begin:col_end] = sub_dna_color()
                    #main dna
                    retval[y-DNA_thickness:y+DNA_thickness+1, col_begin:col_end] = DNA_color
                    

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
                retval[row_begin : row_end, col_begin:col_end] = (_r, _g, _b)

                
            
        self.last_img = retval[:]
        return retval
    
    def last_visualized(self):
        return self.last_img[:]

if __name__ == "__main__":
    vis = Simplest()
    vis.visualize()