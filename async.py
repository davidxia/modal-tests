import asyncio

import modal

app = modal.App("dxia-test-async-input-plane-us-east")


@app.function(experimental_options={"input_plane_region": "us-east"})
async def f(i):
    print(f"function invoked with {i}")
    return i


@app.local_entrypoint()
async def main():
    # execute 10 remote calls to myfunc in parallel
    await asyncio.gather(*[f.remote.aio(i) for i in range(10)])
