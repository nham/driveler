# Driveler

A stupid static site generator in Python 3. Requires pandoc to be available. (It's really just a wrapper around Pandoc)

Driveler itself is just a class. To run it, create a compilation script that imports Driveler:

    from driveler import Driveler

You can then instantiate this in your compilation script:

    d = Driveler()
    d.out_folder = "blah/"
    d.include_dir = "doubleblah/"
    d.site_title = "return of the blah"
    # compilation logic goes here

The three variables listed above are required to be set. `out_folder` is the folder where the HTML/CSS files go after compilation. `site_title` is the name of your blog/site/whatev. `include_dir` should be a folder where HTML templates are kept.


## Why use this when I can use {fancy, feature-filled static site generator}?

Iono. My primary reason is that MathJax support is a must for me and none of the big static site generators seem to support it out of the box. I could probably spend time making MathJax work with one of the other generators, but I figured in the same amount of time I could just create my own script.
