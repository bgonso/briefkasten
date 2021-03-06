from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPNotFound

from dropbox import DropboxContainer
dropbox_container = DropboxContainer()

from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('briefkasten')


def dropbox_factory(request):
    try:
        return dropbox_container.get_dropbox(request.matchdict['drop_id'])
    except KeyError:
        raise HTTPNotFound('no such dropbox')


def dropbox_editor_factory(request):
    dropbox = dropbox_factory(request)
    if dropbox.editor_token == request.matchdict['editor_token']:
        return dropbox
    else:
        raise HTTPNotFound('invalid editor token')


def german_locale(request):
    return 'de'


def main(global_config, **settings):
    """ Configure and create the main application. """
    config = Configurator(settings=settings, locale_negotiator=german_locale)
    config.add_translation_dirs('briefkasten:locale')
    config.add_static_view('briefkasten/static/deform', 'deform:static')
    config.add_static_view('briefkasten/static', 'briefkasten:static')
    config.include('pyramid_deform')
    config.add_route('fingerprint', '/briefkasten/fingerprint')
    config.add_route('dropbox_form', '/briefkasten/submit')
    config.add_route('dropbox_editor', '/briefkasten/{drop_id}/{editor_token}', factory=dropbox_editor_factory)
    config.add_route('dropbox_view', '/briefkasten/{drop_id}', factory=dropbox_factory)
    config.scan()
    dropbox_container.init(settings)
    return config.make_wsgi_app()
