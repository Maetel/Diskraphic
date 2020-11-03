from Visualizer import Simplest, Graphwise
from Navigator import Navigator
import cv2 as cv

def graphwise():
    viz = Graphwise()
    nav = Navigator()
    grayscale = not True
    wid, hi = 500,500
    idx = 0
    while True:
        rt = viz.update(nav.read_next())
        if not rt:
            break
        path, img = f"../../imgs/{idx}.jpg", viz.visualize(wid, hi, grayscale=grayscale)
        cv.imwrite(path, img)
        idx+=1
    stat = viz.stat()
    #(self.elem_idx, self.total_dirs, self.size_max, self.total_size)

    print(f"[Statistics]")
    print(f"\tFile count [{stat[0]}]")
    print(f"\tDirectory count(including root) [{stat[1]}]")
    print(f"\tMaximum file size : [{stat[2]}bytes]")
    print(f"\tTotal file size : [{stat[3]}bytes]")
    result_image = viz.visualize(wid, hi, grayscale=grayscale)
    #cv.imwrite("result/graphwise.jpg", result_image)
    cv.imshow("Result", result_image)
    cv.waitKey(0)

def simplest():
    def print_simplest(list):
        for elem in list:
            print(f"Index[{elem.index}] full path : {elem.full_path}")
    
    viz = Simplest()
    nav = Navigator()
    while viz.update(nav.read_next()):
        pass
    list = viz.visualize()
    print_simplest(list)

def main():
    #simplest()
    graphwise()

if __name__ == "__main__":
    main()