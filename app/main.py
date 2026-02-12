import os
import logging
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from langfuse import Langfuse

from app.db.vector_store import create_vector_store
from app.graph import build_graph
from app.models import ClassificationRequest, ClassificationResponse

# Load environment variables
load_dotenv()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(title="Mini Agent MLOps Project")

# Initialize components
vector_store = create_vector_store()
graph = build_graph()

# Initialize Langfuse
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

    trace = None

    try:
        logger.info(f"Received query: {request.query}")

        # 🔥 Create root trace with input
        trace = langfuse.trace(
            name="mini-agent-trace",
            input={"query": request.query},
            metadata={
                "environment": os.getenv("ENVIRONMENT", "dev"),
                "service": "mini-agent-api"
            }
        )

        # Build state
        state = {
            "query": request.query,
            "vector_store": vector_store,
            "trace": trace
        }

        # Execute LangGraph
        result = graph.invoke(state)

        # 🔥 Update trace with final output
        trace.update(
            output={
                "retrieved_docs": result.get("retrieved_docs"),
                "compliance_result": result.get("compliance_result")
            }
        )

        logger.info("Classification successful")

        return ClassificationResponse(
            query=result.get("query"),
            retrieved_docs=result.get("retrieved_docs"),
            compliance_result=result.get("compliance_result")
        )

    except Exception as e:
        logger.error(f"Error during classification: {str(e)}")

        if trace:
            trace.update(output={"error": str(e)})

        raise HTTPException(status_code=500, detail="Internal processing error")

    finally:
        # 🔥 Important for Azure
        try:
            if trace:
                trace.end()
        except Exception:
            pass

        try:
            langfuse.flush()
        except Exception as flush_error:
            logger.error(f"Langfuse flush failed: {flush_error}")
