from flask import Flask, request
from opentelemetry.trace import set_preferred_tracer_implementation
from opentelemetry.trace import tracer
from opentelemetry.sdk.trace import Tracer
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor
from opentelemetry.context.propagation.tracecontexthttptextformat import (
    TraceContextHTTPTextFormat
)
from opentelemetry.propagators import set_global_httptextformat

app = Flask(__name__)

set_preferred_tracer_implementation(lambda T: Tracer())
tracer = tracer()

tracer.add_span_processor(
    SimpleExportSpanProcessor(ConsoleSpanExporter())
)
set_global_httptextformat(TraceContextHTTPTextFormat)


@app.route("/publish")
def publish():
    hello_str = request.args.get('helloStr')
    print(hello_str)
    return 'published'


if __name__ == "__main__":
    app.run(port=8082)
