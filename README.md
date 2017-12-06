CromlechCromDemo
================

Here we have one of two Crom Demos.  The other one is
[here](https://github.com/Cromlech/Crom_ZODB_SQL_demo) and
includes a cromlech introduction.

This demo  does not use the ZODB, but it does more than the ZODB demo.
It creates a root node, with two leaves.
You have two forms.  One to edit the leaves.  One to login.

There are 4 templates. The layout gives the overall appearance.  There is a
home page tempjlate, a leaf template  with a link to a protected view.  Maybe
the protected view  allows editing the leaf.  And a tabs template.

There is a layout.py file.  It includes a layout object.  And within the
layout there can be two viewlets.  One to show a protected view.  Proably for
editing leaves.  And one to show actions. 

The following files are included.

auth.py
models.py
security.py
wsgi.py
browser
   forms.py
   layout.py
   views.py
   templates
      home.pt
      layout.pt
      leaf.pt
      tabs.pt
      
Installation instructions are below.

For python2.7+
--------------

```bash
$> virtualenv . && source bin/activate
$> python bootstrap.py
$> ./bin/buildout
$> pip install uwsgi
$> uwsgi --http :8080 --wsgi-file app.py
```

For python3.3+
--------------

```bash
$> pyvenv . && source bin/activate
$> python bootstrap.py
$> ./bin/buildout
$> pip install uwsgi
$> uwsgi --http :8080 --wsgi-file app.py
```
To debug the uwsgi easily, just use : --honour-stdin, in the command line when launching it.
it will allow you to use PDB without problems.
You can also reduce the number of workers to 1.
Use the option -p 1

 uwsgi --http :8080 --wsgi-file -p 1 --honour-stdin app.py