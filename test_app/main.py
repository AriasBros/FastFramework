import uvicorn
from fastframework.application import Application

app = Application()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
