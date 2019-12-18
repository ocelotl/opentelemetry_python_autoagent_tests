from flask import Flask
from flask import request

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

app = Flask(__name__)

set_preferred_tracer_implementation(lambda T: Tracer())
tracer = tracer()

tracer.add_span_processor(
    SimpleExportSpanProcessor(ConsoleSpanExporter())
)
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
