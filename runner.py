from cromdemo.wsgi import demo_application
from crom import monkey, implicit
from cromlech.configuration.utils import load_zcml
from cromlech.i18n import load_translations_directories


monkey.incompat()
implicit.initialize()

# read the ZCML
load_zcml("/home/trollfot/projects/devel/CromlechCromDemo/parts/etc/app.zcml")

# load translation
load_translations_directories()

application = demo_application
