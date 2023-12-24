# import neuropacs
from neuropacs.sdk import Neuropacs

def main():
    # api_key = "your_api_key"
    api_key = "m0ig54amrl87awtwlizcuji2bxacjm"
    # server_url = "http://your_server_url:5000"
    server_url = "http://ec2-3-142-212-32.us-east-2.compute.amazonaws.com:5000"
    product_id = "PD/MSA/PSP-v1.0"
    result_format = "TXT"

    # PRINT CURRENT VERSION
    version = Neuropacs.PACKAGE_VERSION

    # INITIALIZE NEUROPACS SDK
    npcs = Neuropacs.init(api_key, server_url)

    # CREATE A CONNECTION   
    connection = npcs.connect()
    print(connection)

    # CREATE A NEW JOB
    order_id = npcs.new_job()
    print(f"order_id: {order_id}")

    # UPLOAD AN IMAGE
    npcs.upload_dataset("../dicom_examples/06_001")

    # START A JOB
    job = npcs.run_job(product_id)
    print(job)

    # # CHECK STATUS
    # status = npcs.check_status()
    # print(status)

    # # GET RESULTS
    # results = npcs.get_results(result_format)
    # print(results)


main()