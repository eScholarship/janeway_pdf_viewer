from django.template.loader import render_to_string
from django.urls import reverse

from plugins.pdf_viewer import logic


def article_pdf_viewer(context):
    """Renders an embedded viewer for the article's PDF galley.

    Reads article and galleys from the journal article template context.
    Only renders for published articles without an HTML galley, since
    article_view_galley 404s before publication and HTML articles already
    show their full text.
    """
    request = context.get('request')
    article = context.get('article')
    if not request or not article or not article.is_published:
        return ''
    if context.get('article_content'):
        return ''

    method = logic.get_method(request)
    if method == logic.METHOD_NONE:
        return ''

    galley = logic.get_pdf_galley(context.get('galleys'))
    if not galley:
        return ''

    pdf_url = reverse('article_view_galley', args=[article.pk, galley.pk])
    template_context = {
        'article': article,
        'galley': galley,
        'pdf_url': pdf_url,
        'absolute_pdf_url': request.build_absolute_uri(pdf_url),
        'download_url': reverse(
            'article_download_galley',
            args=[article.pk, galley.pk],
        ),
        'adobe_client_id': logic.get_setting(
            request.journal,
            'pdf_viewer_adobe_client_id',
        ),
        'method': method,
    }
    return render_to_string(
        'pdf_viewer/{}.html'.format(method),
        template_context,
        request=request,
    )
