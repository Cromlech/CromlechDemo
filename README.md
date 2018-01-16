Cromlech Demo
=============

Support python3.4+ only


Deployment
----------

```bash
$> pyvenv . && source bin/activate
$> pip install -U pip setuptools
$> pip install -r requirements.txt
$> pip install -e .
$> python app.py
```

You can now access http://127.0.0.1:8080 on your browser.
There are 3 users created for the demo purposes:

  - username: admin, password: admin  (all rights)
  - username: demo, password: demo  (view rights)
  - username: grok, password: grok  (no rights)


Demonstrated features
---------------------

  - Encrypted and signed JWT Sessions;
  - Browser components: Layout, Views, Forms and sub components;
  - Publishing using object traversing;
  - Authentication and pluggable security;
  - Internationalization using the Gnu Gettext;
  - Event dispatching;


Documentation
-------------

The technical documentation is within the code itself.
Each part is heavily commented to allow a quick grasp of the purpose
of each piece of software.

You are strongly encouraged to modify and experiment with that demo.


Test coverage
-------------

Every package is thoroughly tested.
You can follow the status of each of them on Travis :
https://travis-ci.org/Cromlech
