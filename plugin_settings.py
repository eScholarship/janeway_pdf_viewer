from utils import plugins
from utils.install import update_settings

PLUGIN_NAME = 'PDF Viewer Plugin'
DISPLAY_NAME = 'PDF Viewer'
DESCRIPTION = 'Embeds PDFs on journal article pages'
AUTHOR = 'California Digital Library'
VERSION = '0.1'
SHORT_NAME = 'pdf_viewer'
MANAGER_URL = 'pdf_viewer_manager'
JANEWAY_VERSION = "1.3.8"


class Pdf_viewerPlugin(plugins.Plugin):
    plugin_name = PLUGIN_NAME
    display_name = DISPLAY_NAME
    description = DESCRIPTION
    author = AUTHOR
    short_name = SHORT_NAME
    manager_url = MANAGER_URL

    version = VERSION
    janeway_version = JANEWAY_VERSION


def install():
    Pdf_viewerPlugin.install()
    update_settings(
        file_path='plugins/pdf_viewer/install/settings.json',
    )


def hook_registry():
    return {
        'article_pdf_viewer': {
            'module': 'plugins.pdf_viewer.hooks',
            'function': 'article_pdf_viewer',
            'name': PLUGIN_NAME,
        },
    }


def register_for_events():
    pass
