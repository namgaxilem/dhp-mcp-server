from fastapi import FastAPI
from routers import hello, proxy  # import proxy

app = FastAPI()


app = FastAPI()

app.include_router(hello.router)
app.include_router(proxy.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)