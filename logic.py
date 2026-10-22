from utils import setting_handler

from plugins.pdf_viewer import plugin_settings

METHOD_NONE = 'none'
METHOD_OBJECT = 'object'
METHOD_EMBED = 'embed'
METHOD_ADOBE = 'adobe'

METHOD_CHOICES = (
    (METHOD_NONE, 'None (no embedded viewer)'),
    (METHOD_OBJECT, '<object> element'),
    (METHOD_EMBED, '<embed> element'),
    (METHOD_ADOBE, 'Adobe PDF Embed API'),
)
METHODS = {value for value, label in METHOD_CHOICES}

# During the PoC, ?pdf_viewer=<method> overrides the journal
# setting so reviewers can compare methods on the same article
OVERRIDE_PARAM = 'pdf_viewer'


def get_setting(journal, setting_name, default=''):
    plugin = plugin_settings.Pdf_viewerPlugin.get_self()
    if not plugin:
        return default
    setting_value = setting_handler.get_plugin_setting(
        plugin,
        setting_name,
        journal,
    )
    if setting_value is None or setting_value.value is None:
        return default
    return setting_value.value


def save_setting(journal, setting_name, value):
    setting_handler.save_plugin_setting(
        plugin_settings.Pdf_viewerPlugin.get_self(),
        setting_name,
        value,
        journal,
    )


def get_method(request):
    override = request.GET.get(OVERRIDE_PARAM)
    if override in METHODS:
        return override
    method = get_setting(request.journal, 'pdf_viewer_method', METHOD_NONE)
    return method if method in METHODS else METHOD_NONE


def get_pdf_galley(galleys):
    if not galleys:
        return None
    return galleys.filter(file__mime_type='application/pdf').first()
