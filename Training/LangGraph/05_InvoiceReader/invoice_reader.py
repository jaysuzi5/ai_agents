from marker.convert import convert_single_pdf
from marker.models import load_all_models
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from typing import TypedDict, List
import json

# Load local models once
model_dict = load_all_models()

class LineItem(BaseModel):
    description: str
    quantity: float = 1.0
    unit_price: float
    total: float

class Invoice(BaseModel):
    invoice_number: str = Field(..., description="Invoice number")
    invoice_date: str
    due_date: str = None
    vendor_name: str
    vendor_address: str = None
    total_amount: float
    subtotal: float = None
    tax: float = None
    currency: str = "USD"
    line_items: List[LineItem] = []

class AgentState(TypedDict):
    markdown: str
    raw_json: str
    parsed: Invoice
    approved: bool

llm = ChatOllama(model="llama3.1:70b", temperature=0, format="json")

def pdf_to_markdown(state):
    full_text, _, _ = convert_single_pdf("/path/to/your/invoice.pdf", model_dict)
    return {"markdown": full_text}

def extract_structured(state):
    prompt = f"""Extract this invoice EXACTLY into the JSON schema below.
    Only output valid JSON, no extra text.

    Invoice markdown:
    {state['markdown'][:12000]}

    Schema:
    {Invoice.model_json_schema()}
    """
    result = llm.invoke(prompt)
    return {"raw_json": result.content}

def parse_and_validate(state):
    data = json.loads(state["raw_json"])
    invoice = Invoice(**data)
    return {"parsed": invoice, "approved": True}

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("ocr", pdf_to_markdown)
workflow.add_node("extract", extract_structured)
workflow.add_node("validate", parse_and_validate)

workflow.set_entry_point("ocr")
workflow.add_edge("ocr", "extract")
workflow.add_edge("extract", "validate")
workflow.add_edge("validate", END)

app = workflow.compile()

# Run it
result = app.invoke({"markdown": "", "raw_json": "", "parsed": None, "approved": False})
print(result["parsed"].model_dump_json(indent=2))