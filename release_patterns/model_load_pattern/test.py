from google.cloud import storage
# import os
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./model_loader/model-magnet-358500-c938d952b597.json"


gcs_bucket = "jeff_ml_system_model_repository"
gcs_model_blob = "iris_svc.onnx"
model_filepath = "./iris_svc.onnx"


client = storage.Client.create_anonymous_client()
bucket = client.bucket(gcs_bucket)
blob = bucket.blob(gcs_model_blob)
blob.download_to_filename(model_filepath)


# storage_client = storage.Client("model-magnet-358500")
# # Create a bucket object for our bucket
# bucket = storage_client.get_bucket("jeff_ml_system_model_repository")
# # Create a blob object from the filepath
# blob = bucket.blob("iris_svc.onnx")
# # Download the file to a destination
# blob.download_to_filename("./iris_svc.onnx")
