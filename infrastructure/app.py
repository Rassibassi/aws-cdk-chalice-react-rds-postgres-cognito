#!/usr/bin/env python3
from aws_cdk import core as cdk

from stacks.chaliceapp import ChaliceApp

app = cdk.App()
ChaliceApp(app, "sampleapp")

app.synth()
