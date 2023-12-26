from collectors import base


class S3Collector(base.Collector):
    def collect(self, context):
        return []


@base.collector
def s3collector(context: base.Context):
    return []
