from flask import Flask, request

from opentelemetry.trace import tracer
from opentelemetry.sdk.trace import Tracer
from opentelemetry import propagators
from opentelemetry.context.propagation.tracecontexthttptextformat import (
    TraceContextHTTPTextFormat
)
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor
from opentelemetry.propagators import set_global_httptextformat
from utils import get_as_list

from opentelemetry.trace import set_preferred_tracer_implementation

set_preferred_tracer_implementation(lambda T: Tracer())
tracer = tracer()

tracer.add_span_processor(
    SimpleExportSpanProcessor(ConsoleSpanExporter())
)
set_global_httptextformat(TraceContextHTTPTextFormat)

print(tracer._active_span_processor._span_processors)

app = Flask(__name__)


@app.route("/format")
def format():

    with tracer.start_as_current_span(
        'format', parent=propagators.extract(get_as_list, request.headers)
    ):
        print(tracer._active_span_processor._span_processors)
        hello_to = request.args.get('helloTo')
        return 'Hello, %s!' % hello_to


if __name__ == "__main__":
    app.run(port=8081)
