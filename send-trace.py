#!/usr/local/bin/python3

from opentelemetry import trace
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

import sys


def sendTrace():
    print("Sending trace to %s..." % otelhost)

    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({SERVICE_NAME: "my-helloworld-service"})
        )
    )
    tracer = trace.get_tracer(__name__)

    # # create a ZipkinExporter
    # # https://opentelemetry-python.readthedocs.io/en/latest/exporter/zipkin/zipkin.html
    # zipkin_exporter = ZipkinExporter(
    #     # version=Protocol.V2
    #     # optional:
    #     # endpoint="http://localhost:9411/api/v2/spans",
    #     # local_node_ipv4="192.168.0.1",
    #     # local_node_ipv6="2001:db8::c001",
    #     # local_node_port=31313,
    #     # max_tag_value_length=256
    #     # timeout=5 (in seconds)
    # )

    # create a JaegerExporter
    # https://opentelemetry-python.readthedocs.io/en/latest/exporter/jaeger/jaeger.html
    jaeger_exporter = JaegerExporter(
        # configure agent
        agent_host_name=otelhost,
        # agent_port=6831,
        agent_port=14268,
        # optional: configure also collector
        collector_endpoint=f'http://{otelhost}:14268/api/traces?format=jaeger.thrift',
        # username=xxxx, # optional
        # password=xxxx, # optional
        # max_tag_value_length=None # optional
    )

    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(jaeger_exporter)
    )

    with tracer.start_as_current_span("processOrder"):
        with tracer.start_as_current_span("applyPayment"):
            with tracer.start_as_current_span("processCreditCard"):
                span = trace.get_current_span()
                span.set_attribute("data.http_response_code", "201")
                span.set_attribute("host.name", "ncc1701d.starfleet.net")
                span.set_attribute("user.name", "Jennifer Lewis")
                span.set_attribute("user.password", "cq239n8-9c")
                span.set_attribute("credit.card.number", "1234-5678-9012-3456")
                span.set_attribute("cvv", "123")
                span.set_attribute("credit.card.expiration.date", "07/13/2026")
                print("Hello world from OpenTelemetry Python!")

    print("Done.")


def main(argv):
    global otelhost

    if len(argv) < 1 or len(argv) > 1:
        print('Usage: tracing.py <OTEL host>')
        sys.exit(-1)

    otelhost = argv[0]
    print('OTEL Host: ', otelhost)
    sendTrace()


if __name__ == "__main__":
    main(sys.argv[1:])
