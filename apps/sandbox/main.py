import asyncio
import os
import sys
import tempfile
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="ThinkBuild Code Execution Sandbox", version="1.0.0")

class CodeExecutionRequest(BaseModel):
    code: str
    timeout_seconds: float = 3.0

class CodeExecutionResponse(BaseModel):
    success: bool
    output: str
    error: str | None = None
    execution_time_seconds: float

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "sandbox"}

@app.post("/run", response_model=CodeExecutionResponse)
async def execute_code(req: CodeExecutionRequest):
    # Security checks: forbid dangerous calls
    forbidden_tokens = [
        "os.system", "subprocess", "shutil.rmtree", "__import__('os')", 
        "socket", "urllib", "requests", "http.client", "open('/etc"
    ]
    for token in forbidden_tokens:
        if token in req.code:
            return CodeExecutionResponse(
                success=False,
                output="",
                error=f"Security Violation: Lệnh '{token}' bị cấm trong Sandbox",
                execution_time_seconds=0.0
            )

    start_time = asyncio.get_event_loop().time()
    
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as tmp_file:
        tmp_file.write(req.code)
        tmp_filename = tmp_file.name

    try:
        proc = await asyncio.create_subprocess_exec(
            sys.executable, tmp_filename,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=req.timeout_seconds)
            execution_time = asyncio.get_event_loop().time() - start_time
            
            out_str = stdout.decode().strip()
            err_str = stderr.decode().strip()
            
            if proc.returncode != 0:
                return CodeExecutionResponse(
                    success=False,
                    output=out_str,
                    error=err_str or f"Process exited with code {proc.returncode}",
                    execution_time_seconds=execution_time
                )
            
            return CodeExecutionResponse(
                success=True,
                output=out_str,
                error=None,
                execution_time_seconds=execution_time
            )
            
        except asyncio.TimeoutError:
            proc.kill()
            return CodeExecutionResponse(
                success=False,
                output="",
                error=f"Timeout: Mã nguồn chạy quá thời gian tối đa ({req.timeout_seconds}s)",
                execution_time_seconds=req.timeout_seconds
            )
    finally:
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)
