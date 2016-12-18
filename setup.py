from distutils.core import setup
import py2exe

setup(
    windows = [
	  
        {
            "script": "gui_interface.pyw",                    ### Main Python script
            "icon_resources": [(0, "ranmaster.ico")],     ### Icon to embed into the PE file.
            'includes': ['lxml.etree', 'lxml._elementpath', 'gzip'],
			}
    ],
)
