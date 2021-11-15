from io import BytesIO

import barcode
from barcode.writer import ImageWriter

from django.core.files.base import ContentFile

#from scan.models import Barcode
#bc = Barcode.obejcts.latest('id')
upc = barcode.get('upc', 123456789, writer=ImageWriter())
i = upc.render() # <PIL.Image.Image image mode=RGB size=523x280 at 0x7FAE2B471320>
image_io = BytesIO()
i.save(image_io, format='PNG')
image_name = 'test.png'
bc.img.save(image_name, content=ContentFile(image_io.getvalue()), save=False)
bc.save()