from raga import *
import pandas as pd
import json
import datetime

def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp

def convert_json_to_data_frame(json_file_path_model_1, json_file_path_model_2, json_file_path_model_3):
    test_data_frame = []
    with open(json_file_path_model_1, 'r') as json_file:
        # Load JSON data
        model_1 = json.load(json_file)
    with open(json_file_path_model_2, 'r') as json_file:
        # Load JSON data
        model_2 = json.load(json_file)
    
    with open(json_file_path_model_3, 'r') as json_file:
        # Load JSON data
        model_gt = json.load(json_file)

    # Create a dictionary to store the inputs and corresponding data points
    inputs_dict = {}
    hr = 1
    # Process model_1 data
    for item in model_1:
        inputs = item["inputs"]
        inputs_dict[tuple(inputs)] = item
    
    # Process model_2 data
    for item in model_2:
        inputs = item["inputs"]
        AnnotationsV1 = ImageDetectionObject()
        ROIVectorsM1 = ROIEmbedding()
        ImageVectorsM1 = ImageEmbedding()
        for index, detection in enumerate(item["outputs"][0]["detections"]):
            id = index+1
            AnnotationsV1.add(ObjectDetection(Id=id, ClassId=0, ClassName=detection['class'], Confidence=detection['confidence'], BBox= detection['bbox'], Format="xywh_normalized"))
            ROIVectorsM1.add(id=id, embedding_values=[float(num_str) for num_str in detection['roi_embedding']])
                
            attributes_dict = {}
            attributes = item.get("attributes", {})
            for key, value in attributes.items():
                attributes_dict[key] = StringElement(value)
            image_embeddings = item.get("image_embedding", {})
            for value in image_embeddings:
                ImageVectorsM1.add(Embedding(float(value)))

        merged_item = inputs_dict.get(tuple(inputs), {})
        AnnotationsV2 = ImageDetectionObject()
        ROIVectorsM2 = ROIEmbedding()
        ImageVectorsM2 = ImageEmbedding()
        for index, detection in enumerate(merged_item["outputs"][0]["detections"]):
            id = index+1
            AnnotationsV2.add(ObjectDetection(Id=id, ClassId=0, ClassName=detection['class'], Confidence=detection['confidence'], BBox= detection['bbox'], Format="xywh_normalized"))
            ROIVectorsM2.add(id=id, embedding_values=[float(num_str) for num_str in detection['roi_embedding']])
        
        image_embeddings = merged_item.get("image_embedding")
        for value in image_embeddings:
            ImageVectorsM2.add(Embedding(float(value)))
        
        merged_item2 = inputs_dict.get(tuple(inputs))
        AnnotationsV3 = ImageDetectionObject()
        ROIVectorsM3 = ROIEmbedding()
        ImageVectorsM3 = ImageEmbedding()
        for index, detection in enumerate(merged_item2["outputs"][0]["detections"]):
            id = index+1
            AnnotationsV3.add(ObjectDetection(Id=id, ClassId=0, ClassName=detection['class'], Confidence=detection['confidence'], BBox= detection['bbox'], Format="xywh_normalized"))
            ROIVectorsM3.add(id=id, embedding_values=[float(num_str) for num_str in detection['roi_embedding']])
        
        image_embeddingsGT = merged_item2.get("image_embedding")
        for value in image_embeddingsGT:
            ImageVectorsM3.add(Embedding(float(value)))


        data_point = {
            'ImageUri':StringElement(item["image_url"]),
            'ImageId': StringElement(item["inputs"][0]),
            'TimeOfCapture': TimeStampElement(get_timestamp_x_hours_ago(hr)),
            'AnnotationsV1': AnnotationsV1,
            'ROIVectorsM1': ROIVectorsM1,
            'ImageVectorsM1': ImageVectorsM1,
            'AnnotationsV2': AnnotationsV2,
            'ROIVectorsM2': ROIVectorsM2,
            'ImageVectorsM2': ImageVectorsM2,
            'AnnotationsV3': AnnotationsV3,
            'ROIVectorsM3': ROIVectorsM3,
            'ImageVectorsM3': ImageVectorsM3,
            
        }

        merged_dict = {**data_point, **attributes_dict}
        test_data_frame.append(merged_dict)
        hr+=1

    return test_data_frame



#Convert JSON dataset to pandas Data Frame
pd_data_frame = pd.DataFrame(convert_json_to_data_frame("ma.json", "mb.json", "gt.json"))
#pd_data_frame.to_pickle("TestingDataFrame.pkl")

schema = RagaSchema()
schema.add("ImageUri", ImageUriSchemaElement())
schema.add("ImageId", PredictionSchemaElement())
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement())
schema.add("Reflection", AttributeSchemaElement())
schema.add("Overlap", AttributeSchemaElement())
schema.add("CameraAngle", AttributeSchemaElement())
schema.add("AnnotationsV1", InferenceSchemaElement(model="modelA"))
schema.add("ImageVectorsM1", ImageEmbeddingSchemaElement(model="modelA"))
schema.add("ROIVectorsM1", RoiEmbeddingSchemaElement(model="modelA"))
schema.add("AnnotationsV2", InferenceSchemaElement(model="modelB"))
schema.add("ImageVectorsM2", ImageEmbeddingSchemaElement(model="modelB"))
schema.add("ROIVectorsM2", RoiEmbeddingSchemaElement(model="modelB"))
schema.add("AnnotationsV3", InferenceSchemaElement(model="modelGT"))
schema.add("ImageVectorsM3", ImageEmbeddingSchemaElement(model="modelGT"))
schema.add("ROIVectorsM3", RoiEmbeddingSchemaElement(model="modelGT"))


project_name = "testingProject" # Project Name
run_name= "VS_pd_exp_19Sep_v06" # Experiment Name should always be unique
dataset_name = "DSPandas" # Dataset Name


#create test_session object of TestSession instance
test_session = TestSession(project_name=project_name,run_name=run_name)

#create test_ds object of Dataset instance
test_ds = Dataset(test_session=test_session, name=dataset_name,data=pd_data_frame,schema=schema)

#load schema and pandas data frame
test_ds.load()

# Params for labelled AB Model Testing
testName = "QA_Labelled_19SepV1"
modelA = "modelA"
modelB = "modelB"
gt = "modelGT"
type = "labelled"
aggregation_level = ["Reflection","Overlap","CameraAngle"]
rules = ModelABTestRules()
rules.add(metric ="precision", IoU = 0.5, _class = "ALL", threshold = 0.5)
rules.add(metric ="f1score", IoU = 0.5, _class = "ALL", threshold = 0.5)
rules.add(metric ="recall", IoU = 0.5, _class = "ALL", threshold = 0.5)
# rules.add(metric = "precision", IoU = 0.5, _class = "candy", threshold = 0.5)

#create payload for model ab testing
model_comparison_check = model_ab_test(test_session, dataset_name=dataset_name, test_name=testName, modelA = modelA , modelB = modelB ,aggregation_level = aggregation_level, type = type,  rules = rules, gt=gt)


#add payload into test_session object
test_session.add(model_comparison_check)


# # Params for unlabelled AB Model Testing
testName = "QA_Unlabelled_19SepV1"
modelA = "modelA"
modelB = "modelB"
type = "unlabelled"
aggregation_level = ["Reflection","Overlap","CameraAngle"]
rules = ModelABTestRules()
rules.add(metric ="difference_all", IoU = 0.5, _class = "ALL", threshold = 0.5)
rules.add(metric = "difference_candy", IoU = 0.5, _class = "candy", threshold = 0.5)


# #create payload for model ab testing
model_comparison_check = model_ab_test(test_session, dataset_name=dataset_name, test_name=testName, modelA = modelA , modelB = modelB , type = type, aggregation_level = aggregation_level, rules = rules)


# #add payload into test_session object
test_session.add(model_comparison_check)

#run added ab test model payload
test_session.run()