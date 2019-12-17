from flask import Flask, request

from opentelemetry.sdk.trace import Tracer
from opentelemetry import propagators
from opentelemetry.context.propagation.tracecontexthttptextformat import (
    TraceContextHTTPTextFormat
)
from opentelemetry.propagators import set_global_httptextformat
from utils import get_as_list


app = Flask(__name__)

tracer = Tracer('formatter')

set_global_httptextformat(TraceContextHTTPTextFormat)


@app.route("/format")
def format():

    with tracer.start_span(
        'format', parent=propagators.extract(get_as_list, request.headers)
    ):
        hello_to = request.args.get('helloTo')
        return 'Hello, %s!' % hello_to


if __name__ == "__main__":
    app.run(port=8081)
