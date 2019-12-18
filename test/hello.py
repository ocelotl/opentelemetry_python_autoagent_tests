import requests
import sys
import time
from flask import Flask

from opentelemetry.trace import tracer
from opentelemetry.sdk.trace import Tracer
from opentelemetry import propagators
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor
from opentelemetry.context.propagation.tracecontexthttptextformat import (
    TraceContextHTTPTextFormat
)
from opentelemetry.propagators import set_global_httptextformat
from opentelemetry.trace import set_preferred_tracer_implementation

app = Flask(__name__)

set_preferred_tracer_implementation(lambda T: Tracer())
tracer = tracer()

tracer.add_span_processor(
    SimpleExportSpanProcessor(ConsoleSpanExporter())
)
set_global_httptextformat(TraceContextHTTPTextFormat)


def http_get(port, path, param, value):

    headers = {}
    propagators.inject(tracer, dict.__setitem__, headers)

    r = requests.get(
        'http://localhost:{}/{}'.format(port, path),
        params={param: value},
        headers=headers
    )

    assert r.status_code == 200
    return r.text


assert len(sys.argv) == 2

hello_to = sys.argv[1]

with tracer.start_as_current_span('hello') as hello_span:

    with tracer.start_as_current_span('hello-format', parent=hello_span):
        hello_str = http_get(8081, 'format', 'helloTo', hello_to)

    with tracer.start_as_current_span('hello-publish', parent=hello_span):
        http_get(8082, 'publish', 'helloStr', hello_str)

# yield to IOLoop to flush the spans
time.sleep(2)
