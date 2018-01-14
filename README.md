Cromlech Demo
=============

Support python3.4+ only


Deployment
----------

```bash
$> pyvenv . && source bin/activate
$> python bootstrap.py
$> ./bin/buildout
$> pip install uwsgi
$> uwsgi --http :8080 --wsgi-file app.py
```


Features
--------

  - Encrypted and signed JWT Sessions;
  - Layout, Views, Forms;
  - Publishing using object traversing;
  - Pluggable security;
  - Internationalization using the Gnu Gettext
