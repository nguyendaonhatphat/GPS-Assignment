
import logging
import json
from datetime import datetime, timezone

import azure.functions as func

app = func.FunctionApp()

@app.timer_trigger(
    schedule="0 */5 * * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False
)
@app.blob_output(
    arg_name="output",
    path="gps-data/gps-location.json",
    connection="GPS_STORAGE"
)
def GPSFunction(
    myTimer: func.TimerRequest,
    output: func.Out[str]
) -> None:

    if myTimer.past_due:
        logging.info("The timer is past due!")

    # Simulated GPS data
    gps_data = {
        "device_id": "gps-sensor-vgu",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "gps": {
            "lat": 10.8231,
            "lon": 106.6297
        }
    }

    # Convert data to JSON
    blob_content = json.dumps(gps_data, indent=4)

    # Send JSON data to Azure Blob Storage
    output.set(blob_content)

    logging.info("GPS data generated successfully.")
    logging.info(blob_content)
