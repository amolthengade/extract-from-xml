from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
from excel_extractor import parse_tally_xml, save_to_excel

app = FastAPI()


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  

@app.post("/upload/")
async def process_xml(file: UploadFile = File(...)):

    xml_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(xml_path, "wb") as buffer:
        buffer.write(await file.read())  

    transactions = parse_tally_xml(xml_path)
    if not transactions:
        return {"message": "No 'Receipt' transactions found."}

    output_file = os.path.join(UPLOAD_FOLDER, "Tally_Receipts.xlsx")
    save_to_excel(transactions, output_file)

    return FileResponse(output_file, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename="Tally_Receipts.xlsx")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
