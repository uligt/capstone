from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Request
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from pydantic import BaseModel, Field
from typing import List, Dict
import urllib.request
import itertools
import json

app = FastAPI()

# ---------- Request and response models ---------- #
class OrderDetails(BaseModel):
    garmentType: str = Field(..., examples=["Shirt", "Pants"])
    material: str = Field(..., examples=["Cotton", "Polyester"])
    unitWeight: float = Field(..., gt=0, examples=[0.30, 1.20])
    size: str = Field(..., examples=["XS", "S", "M", "L", "XL"])
    collection: str = Field(..., examples=["Summer", "Winter"])

class PackagingConfigurations(BaseModel):
    unitsPerPackage: int = Field(..., gt=0, examples=[1, 5, 10])
    foldingMethod: str = Field(..., examples=["Method1", "Method2"])
    layout: str = Field(..., examples=["LayoutA", "LayoutB"])
    supplier: str = Field(..., examples=["SupplierA", "SupplierB"])

# ---------- Network definitions ---------- #
url = 'https://pckg-quality-endpoint.eastus.inference.ml.azure.com/score'
api_key = ''
headers = {'Content-Type':'application/json', 'Accept': 'application/json', 'Authorization':('Bearer '+ api_key)}

# ---------- Helper functions ---------- #
def build_request_data(orderDetails: OrderDetails):
    COLUMNS = [
        "SupplierName", "GarmentType", "Material", "Weight",
        "ProposedUnitsPerCarton", "ProposedFoldingMethod",
        "ProposedLayout", "Size", "Collection"
    ]

    GARMENT_TYPE = orderDetails.garmentType
    MATERIAL = orderDetails.material
    WEIGHT = orderDetails.unitWeight
    SIZE = orderDetails.size
    COLLECTION = orderDetails.collection


    FOLDING_METHODS = ["Method1", "Method2", "Method3"]
    LAYOUTS = ["LayoutA", "LayoutB", "LayoutC", "LayoutD", "LayoutE"]
    UNITS_RANGE = list(range(5, 50, 5))
    SUPPLIERS = [
        "SupplierA", "SupplierB", "SupplierC", "SupplierD",
        "SupplierE", "SupplierF", "SupplierG", "SupplierH"
    ]

    data_rows = [
        [
            supplier,
            GARMENT_TYPE,
            MATERIAL,
            WEIGHT,
            units,
            folding,
            layout,
            SIZE,
            COLLECTION,
        ]
        for supplier, units, folding, layout in itertools.product(
            SUPPLIERS,
            UNITS_RANGE,
            FOLDING_METHODS,
            LAYOUTS,
        )
    ]

    request_data = {
        "input_data": {
            "index": [0, 1],
            "columns": COLUMNS,
            "data": data_rows,
        }
    }

    return request_data



def execute_request(body):
    url = 'https://pckg-quality-endpoint.eastus.inference.ml.azure.com/score'
    
    api_key = ''
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")


    headers = {'Content-Type':'application/json', 'Accept': 'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        return response
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))

def to_packaging_config(packaging_detail: List) -> PackagingConfigurations:
    supplier, _, _, _, units, folding, layout, *_ = packaging_detail
    return PackagingConfigurations(
        unitsPerPackage=units,
        foldingMethod=folding,
        layout=layout,
        supplier=supplier
    )


def build_configurations(request_data, result) -> List[PackagingConfigurations]:
    packaging_details = request_data["input_data"]["data"]

    packaging_details_enriched = [order + [score]
                for order, score in zip(packaging_details, result)]
        
    best_overall = max(packaging_details_enriched, key=lambda r: r[-1])

    best_per_supplier: Dict[str, List] = {}
    for detail in packaging_details_enriched:
        supplier, *_, score = detail
        if supplier not in best_per_supplier or score > best_per_supplier[supplier][-1]:
            best_per_supplier[supplier] = detail

    configs: List[PackagingConfigurations] = []
    configs.append(to_packaging_config(best_overall))

    for entry in best_per_supplier.values():
        configs.append(to_packaging_config(entry))

    return configs



# ---------- Endpoints ---------- #
@app.post("/packaging-configs", response_model=List[PackagingConfigurations], status_code=201)
async def packaging_configs(data: OrderDetails) -> List[PackagingConfigurations]:
    request_data = build_request_data(data)
    body = str.encode(json.dumps(request_data))
    response = execute_request(body)
    result = json.loads(response.read()) # array of float values
    
    configurations = build_configurations(request_data, result)

    return configurations
    

@app.post("/audit")
async def process_excel(
    threshold: float = Query(..., description="Threshold value to filter numeric cells"),
    file: UploadFile = File(..., description="Excel file to process (.xls or .xlsx)")
):
    # Ensure we got an Excel file
    if not file.filename.lower().endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="File must be an Excel document")

    # Read the uploaded file into a pandas DataFrame
    try:
        contents = await file.read()
        df = pd.read_excel(contents, engine='openpyxl')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading Excel file: {e}")

    # Example processing: filter numeric columns for any value > threshold
    numeric_cols = df.select_dtypes(include="number").columns
    if numeric_cols.empty:
        return JSONResponse(
            status_code=200,
            content={"message": "No numeric columns found", "threshold": threshold}
        )

    # Build a mask: rows where at least one numeric cell exceeds the threshold
    mask = df[numeric_cols].gt(threshold).any(axis=1)
    filtered = df[mask]

    # Convert filtered DataFrame to JSON-friendly structure
    result = filtered.to_dict(orient="records")

    return {
        "threshold": threshold,
        "total_rows": len(df),
        "rows_above_threshold": len(filtered),
        "filtered_data": result
    }