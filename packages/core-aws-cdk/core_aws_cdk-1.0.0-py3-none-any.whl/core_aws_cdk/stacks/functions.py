# -*- coding: utf-8 -*-

from typing import Dict, Optional, List

from aws_cdk import Duration
from aws_cdk.aws_lambda import Architecture
from aws_cdk.aws_lambda import Runtime, IEventSource
from aws_cdk.aws_lambda_python_alpha import PythonFunction

from core_aws_cdk.stacks.base import BaseStack


class BaseLambdaStack(BaseStack):
    """ It contains the base elements to create Lambda infrastructure on AWS """

    def create_lambda_python(
            self, function_id: str, function_name: str,
            entry_point: str, index: str = "handler.py", handler: str = "handler",
            timeout: Duration = Duration.minutes(5), runtime: Runtime = Runtime.PYTHON_3_11,
            architecture: Architecture = Architecture.ARM_64, event_sources: Optional[List[IEventSource]] = None,
            environment: Dict = None, **kwargs) -> PythonFunction:

        """
        It creates a Lambda Function based on Python. Use this method if your function
        does NOT contain external dependencies that requires authentication or when
        it does NOT require specific deployment requirements when creating the
        function package...
        """

        fcn = PythonFunction(
            scope=self, id=function_id, function_name=function_name,
            index=index, entry=entry_point, handler=handler,
            runtime=runtime, architecture=architecture,
            environment=environment, timeout=timeout,
            **kwargs)

        if event_sources:
            for source in event_sources:
                fcn.add_event_source(source)

        return fcn
