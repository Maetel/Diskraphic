# Diskraphic

- Analyzes your file system and visualizes it into a graphical form
- This toy project is my 2nd python tutorial

## Initial try - Graphwise

Let's begin with the simplest style.  
The longer(the darker), the larger file size.  
_FYI : Result image directory is excluded from the analysis_

- **Grayscale** - Background intensity is the mean file size.
- **RGB** - File size as Red, file name as Green, path as Blue. Of similar color means they're near in path.
  ![Graphwise](result/graphwise_gray.gif) ![Graphwise](result/graphwise_rgb.gif)

## Dependency

> Python3.8 (possibly lower versions of Python3 will fit)  
> OpenCV (possibly any version will fit)

## Example

- **Graphwise** - shown as above

  > ```python
  > from Visualizer import Graphwise
  > from Navigator import Navigator
  >
  > path = "" #if not designated, set it to current path
  > viz = Graphwise()
  > nav = Navigator(path)
  > while viz.update(nav.read_next()):
  >    pass
  > stat = viz.stat()
  > result_image = viz.visualize()
  > ```

- **Simplest** - returns a list, filled with all the materials
  > ```python
  > from Visualizer import Simplest
  > from Navigator import Navigator
  >
  > path = "" #if not designated, set it to current path
  > viz = Simplest()
  > nav = Navigator(path)
  > while viz.update(nav.read_next()):
  >    pass
  > result_list = viz.visualize()
  > ```

### These are the brainstorming materials

##### Core logic

1. A file is placed under a certain path.
1. A path is a child of another path, unless it's the root directory
1. A file has following attributes
   - name
   - type (extension)
   - size
   - some attributes like date created/modified, author
1. A file may require permission to even access
1. Directory structure is in a tree form.
1. There will be one or more drives, and each drive will become a root.
1. **_How to turn file attributes into color channels and its position related to previous files is the key_**

##### overall

1. an image can be in grayscale (8bytes) or can be in rgb (24bytes) or rgba(32bytes)
   - how to visualize file attributes and directory structure is the main key
1. Used
1. **_The final image must be updatable for each iteration._** With this logic, I can extract the result each iteration, so that I can visualize it in a video form. Here is the pseudo code for the logic;

```python
while True:
  info = read_next_file()
  if info:
    update_result(info)
  else:
    break
```

##### Just ideas

1. The result can be a tree (or trees for multiple drives), growing as the iteration goes on. Inaccessible dirs and files will be the root, it being the mass of inaccessible files' size compared to that of the accessibles.  
   ![Tree](https://library.kissclipart.com/20180918/yeq/kissclipart-tree-grayscale-clipart-fir-grayscale-black-and-whi-1853b094d5b499c2.png)
1. The result can be a disk (such traditional huh).  
   ![Sonic wave](https://i.pinimg.com/originals/e2/65/15/e2651599c39a96d329e982fd0a169c51.png)  
   ![Disk usage](https://i.stack.imgur.com/42Daj.jpg)
1. Or some kind of fractal pattern will be cool  
   ![Fractal](https://cdn.shopify.com/s/files/1/0080/9176/2784/files/fractal_intro_grande.jpg?v=1549797078)
1. Recursive design. Just google it. There are tons  
   ![Recursive](https://i.pinimg.com/564x/0f/74/b7/0f74b792a692853a8bec3bc25788189f.jpg)
1. Let's just begin from a small step. Don't impress myself too much from the beginning. Just do it.
