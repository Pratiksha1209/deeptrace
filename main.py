from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.engine.pipeline import StreamingRiskEvaluator
import json

app = FastAPI(title="DeepTrace Gateway")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"status": "DEEPTRACE_ONLINE"}

@app.websocket("/ws/audio")
async def audio_socket(ws: WebSocket):
    await ws.accept()
    evaluator = StreamingRiskEvaluator()
    try:
        while True:
            data = await ws.receive_bytes()
            result = evaluator.process_chunk(data)
            await ws.send_text(json.dumps(result))
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
