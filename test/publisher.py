from flask import Flask
from flask import request

from opentelemetry.sdk.trace import Tracer
from opentelemetry import propagators
from opentelemetry.context.propagation.tracecontexthttptextformat import (
    TraceContextHTTPTextFormat
)
from opentelemetry.propagators import set_global_httptextformat
from utils import get_as_list

app = Flask(__name__)

tracer = Tracer('publisher')

set_global_httptextformat(TraceContextHTTPTextFormat)


@app.route("/publish")
def publish():

    with tracer.start_as_current_span(
        'publish', propagators.extract(get_as_list, request.headers)
    ):
        hello_str = request.args.get('helloStr')
        print(hello_str)
        return 'published'


if __name__ == "__main__":
    app.run(port=8082)
