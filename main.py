import asyncio
import logging.config
from io import StringIO

import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

from config_loader import ConfigLoader
from risk_processor.input_validator import InputValidator
from risk_processor.risk_processor import RiskProcessor

cfg = ConfigLoader().load()
logging.config.dictConfig(cfg['logging'])
logger = logging.getLogger(__name__)

noise_level = cfg['risk']['noise_level']
weights = cfg['risk']['weights']
app = FastAPI(title='Risk Processor Service')


@app.post('/process')
def process_json(payload: dict):
    try:
        valid = InputValidator.validate_json(payload)
        raw = valid.dict(exclude={'city'})
        processor = RiskProcessor(weights=weights, noise_level=noise_level)
        result = processor.process(raw)
        logger.info(f"Processed {valid.city}: score={result['risk_score']}")
        return {'city': valid.city, **result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Processing error: {e}")
        raise HTTPException(status_code=500, detail='Internal processing error')


@app.post('/process-csv')
async def process_csv(file: UploadFile = File(...)):
    content = (await file.read()).decode()
    rows = list(InputValidator.parse_csv(content))

    async def handle_row(idx, data, err):
        if err:
            return {'row': idx, 'error': err}
        try:
            processor = RiskProcessor(weights=weights or {}, noise_level=noise_level)
            out = processor.process(data)
            out['row'] = idx
            return out
        except Exception as e:
            logger.warning(f"Row {idx} processing error: {e}")
            return {'row': idx, 'error': str(e)}

    tasks = [handle_row(i, data, err) for i, data, err in rows]
    results = await asyncio.gather(*tasks)

    df = pd.DataFrame(results)
    buf = StringIO()
    df.to_csv(buf, index=False)
    buf.seek(0)
    return StreamingResponse(buf, media_type='text/csv',
                             headers={'Content-Disposition': 'attachment; filename=results.csv'})
