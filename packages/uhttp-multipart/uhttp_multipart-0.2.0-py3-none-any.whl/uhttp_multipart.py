from multipart.multipart import FormParser, parse_options_header
from multipart.exceptions import FormParserError
from uhttp import App, MultiDict, Response


def parse_form(request):
    form = MultiDict()

    def on_field(field):
        form[field.field_name.decode()] = field.value.decode()

    def on_file(file):
        if file.field_name:
            form[file.field_name.decode()] = file.file_object

    content_type, options = parse_options_header(
        request.headers.get('content-type', '')
    )

    try:
        parser = FormParser(
            content_type.decode(),
            on_field,
            on_file,
            boundary=options.get(b'boundary'),
            config={'MAX_MEMORY_FILE_SIZE': float('inf')}  # app._max_content
        )
        parser.write(request.body)
        parser.finalize()
    except FormParserError:
        raise Response(400)

    return form


def multipart():
    app = App()

    @app.before
    def multipart_support(request):
        if 'multipart/form-data' in request.headers.get('content-type'):
            request.form = parse_form(request)

    return app
