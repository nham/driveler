% About Driveler

A stupid static site generator in Python 3. Requires pandoc to be available. (It's really just a wrapper around Pandoc)

Driveler itself is just a class. To run it, create a compilation script that imports Driveler:

```` python
    from driveler import Driveler
````

You can then instantiate this in your compilation script:

```` python
    d = Driveler()
    d.out_folder = "blah/"
    d.include_dir = "doubleblah/"
    d.site_title = "return of the blah"
    # compilation logic goes here
````

You can set a variety of parameters when compiling. So far, only `include_dir` is required. It is the folder where HTML templates are kept.`out_folder` is the folder where the HTML/CSS files go after compilation. It defaults to "_out/". `site_title` is the name of your blog/site/whatev, and will show up as a prefix in the HTML page title, like "site_title - page_title".  You can also use a css file by setting `css_file`.

Note that driveler uses the pandoc_title_block extension, so you can set author, page title and date for each page. Please check the Pandoc documents for more details.


## Why use this when I can use {fancy, feature-filled static site generator}?

Iono. My primary reason is that MathJax support is a must for me and none of the big static site generators seem to support it out of the box. I could probably spend time making MathJax work with one of the other generators, but I figured in the same amount of time I could just create my own script.
