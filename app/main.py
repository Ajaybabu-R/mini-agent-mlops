import os
import logging
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from langfuse import Langfuse

from app.db.vector_store import create_vector_store
from app.graph import build_graph
from app.models import ClassificationRequest, ClassificationResponse

load_dotenv()

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Mini Agent MLOps Project")

vector_store = create_vector_store()
graph = build_graph()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/classify", response_model=ClassificationResponse)
async def classify_product(request: ClassificationRequest):

    try:
        logger.info(f"Received query: {request.query}")

        trace = langfuse.trace(name="mini-agent-trace")

        state = {
            "query": request.query,
            "vector_store": vector_store,
            "trace": trace
        }

        result = graph.invoke(state)

        trace.update(output=result)

        response = ClassificationResponse(
            query=result.get("query"),
            retrieved_docs=result.get("retrieved_docs"),
            compliance_result=result.get("compliance_result")
        )

        logger.info("Classification successful")

        return response

    except Exception as e:
        logger.error(f"Error during classification: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal processing error")
