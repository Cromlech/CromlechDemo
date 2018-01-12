Cromlech Demo
=============

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

To debug uwsgi with `pdb` use the `--honour-stdin` option.
You can also reduce the number of workers to 1 with the option `-p 1`.

```bash
$> uwsgi --http :8080 --wsgi-file -p 1 --honour-stdin app.py
```
