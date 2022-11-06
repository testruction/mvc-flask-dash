from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor, BatchSpanProcessor

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from opentelemetry.sdk.extension.aws.trace import AwsXRayIdGenerator

from opentelemetry.instrumentation.botocore import BotocoreInstrumentor

import pg8000
from opentelemetry.instrumentation.dbapi import trace_integration
from project.utils import get_openid_user


def init_tracer(args):
    """
    Tracing configuration using OpenTelemetry
    """
    resource = Resource.create(attributes={"service.namespace": "io.testruction",
                                           "service.name": "mvc-flask-dash"})
    
    trace.set_tracer_provider(TracerProvider(id_generator=AwsXRayIdGenerator(),
                                             resource=resource))

    otlp_exporter = OTLPSpanExporter()
    otlp_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(otlp_processor)

    if args.trace_stdout:
        trace.get_tracer_provider().add_span_processor(
            SimpleSpanProcessor(ConsoleSpanExporter()))
    
    #set open telemetry for botocore
    def request_hook(span: trace.get_current_span(), service_name, operation_name, api_params):
        if span and span.is_recording():
            span.set_attribute("enduser.id", get_openid_user())

    BotocoreInstrumentor().instrument(request_hook=request_hook)

    trace_integration(connect_module=pg8000,
                      connect_method_name="connect",
                      database_system="postgresql")
