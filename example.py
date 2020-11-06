from Visualizer import Simplest, Graphwise
from Navigator import Navigator
import cv2 as cv
from PIL import Image
import sys

def is_gui():
    if sys.stdin.isatty():
        print("No gui environment")
        return False
    return True

def graphwise():
    #setup
    viz = Graphwise()
    nav = Navigator()
    grayscale = True
    DNA_ish = not True
    wid, hi = 400,400
    gif_path = f'result/{"DNA" if DNA_ish else "graphwise"}_{"gray" if grayscale else "rgb"}.gif'
    gif_duration = 4 #seconds
    images = []
    cv_cvt_format = cv.COLOR_GRAY2RGB if grayscale else cv.COLOR_BGR2RGB
    def cv_img_to_PIL_img(cv_img):
        return Image.fromarray(cv.cvtColor(cv_img, cv_cvt_format))

    #main logic
    while viz.update(nav.read_next()):
        cv_img = viz.visualize(wid, hi, grayscale=grayscale, DNA_ish=DNA_ish)
        images.append(cv_img_to_PIL_img(cv_img))
        pass

    #view results
    stat = viz.stat()

    print(f"[Statistics]")
    print(f"\tFile count [{stat[0]}]")
    print(f"\tDirectory count(including root) [{stat[1]}]")
    print(f"\tMaximum file size : [{stat[2]}bytes]")
    print(f"\tTotal file size : [{stat[3]}bytes]")

    if images:
        print("Creating gif...")
        images[0].save(gif_path, save_all=True, append_images=images[1:], optimize=True, duration=int((gif_duration*1000)/len(images)), loop=0)
        print("GIF saving done")
    
    if is_gui():
        cv.imshow("Result", viz.visualize(wid, hi, grayscale=grayscale, DNA_ish=DNA_ish))
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
