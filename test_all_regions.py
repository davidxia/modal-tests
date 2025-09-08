"""
Test all worker regions.
"""

import os
import subprocess
import modal

INPUT_PLANE_REGIONS = ["us-east", "us-west", "eu-west", "ap-south"]
APP_NAME = "dxia-test-cls-with-options"

app = modal.App(APP_NAME)


@app.cls()
class MyClass:
    @modal.method()
    def f(self) -> str:
        return f"function invoked in cloud {os.getenv('MODAL_CLOUD_PROVIDER', 'unknown')}, region {os.getenv('MODAL_REGION', 'unknown')}"


@app.local_entrypoint()
def main():
    with modal.enable_output():
        app.deploy()

    for region in INPUT_PLANE_REGIONS:
        c = modal.Cls.from_name(APP_NAME, "MyClass").with_options(region=region)
        print(c().f.remote())

    subprocess.run(["modal", "app", "stop", APP_NAME], check=True)
