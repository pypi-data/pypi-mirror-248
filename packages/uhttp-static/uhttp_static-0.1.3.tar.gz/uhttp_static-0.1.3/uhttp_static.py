import os
from mimetypes import guess_type
from uhttp import App, Response


def send_file(path):
    if not os.path.isfile(path):
        raise RuntimeError('Invalid file')

    mime_type = guess_type(path)[0] or 'application/octet-stream'

    with open(path, 'rb') as file:
        content = file.read()

    return Response(
        status=200,
        headers={'content-type':  mime_type},
        body=content
    )


def static(directory='.'):
    directory = os.path.realpath(directory)
    if not os.path.isdir(directory):
        raise RuntimeError('Invalid directory')

    app = App()

    @app.get('/(?P<static>.*)')
    def _static(request):
        path = os.path.realpath(
            os.path.join(directory, request.params['static'])
        )
        if os.path.commonpath([directory, path]) == directory:
            if os.path.isfile(path):
                return send_file(path)
            if os.path.isdir(path):
                index = os.path.join(path, 'index.html')
                if os.path.isfile(index):
                    return send_file(index)
        return 404

    return app
