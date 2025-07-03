from fastapi import FastAPI
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
    

