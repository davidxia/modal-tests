import modal

image = modal.Image.debian_slim().pip_install("fastapi[standard]")
app = modal.App(name="dxia-test-web-endpoint", image=image)


@app.function(experimental_options={"input_plane_region": "us-east"})
@modal.fastapi_endpoint(docs=True)
def hello():
    return "Hello world!"


@app.function(experimental_options={"input_plane_region": "us-east"})
@modal.fastapi_endpoint(docs=True)
def greet(user: str) -> str:
    return f"Hello {user}!"
