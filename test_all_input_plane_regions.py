"""
Test all input plane regions.

We do it this way because
modal.Cls.with_options() doesn't support experimental_options yet.
One can't do this.
c = modal.Cls.from_name(APP_NAME, "MyClass").with_options(experimental_options={"input_plane_region": region})
"""

import os
import modal


INPUT_PLANE_REGIONS = ["us-east", "us-west", "eu-west", "ap-south"]
app = modal.App()


def f() -> str:
    return f"function invoked in cloud {os.getenv('MODAL_CLOUD_PROVIDER', 'unknown')}, region {os.getenv('MODAL_REGION', 'unknown')}"


if __name__ == "__main__":
    region_functions = {}
    for region in INPUT_PLANE_REGIONS:
        region_functions[region] = app.function(
            name=f"{region}_f", serialized=True, experimental_options={"input_plane_region": region}
        )(f)

    with modal.enable_output():
        with app.run():
            for region, region_f in region_functions.items():
                print(region, region_f.remote())
