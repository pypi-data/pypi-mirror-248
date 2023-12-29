from raga import *
import pandas as pd
import json
import time

# ds_json_file = "train_modelB.json"
# ds_json_file1 = "field_modelB.json"

# model_name = "Train"
# model_name1 = "Field"


# test_df = []
# with open(ds_json_file, 'r') as json_file:
#     # Load JSON data
#     json_data = json.load(json_file)
    
#     # Process the JSON data
#     transformed_data = []
#     for item in json_data:
#         AnnotationsV1 = ImageDetectionObject()
#         ROIVectorsM1 = ROIEmbedding()
#         ImageVectorsM1 = ImageEmbedding()
#         for index, detection in enumerate(item["outputs"][0]["detections"]):
#             id = index+1
#             AnnotationsV1.add(ObjectDetection(Id=id, ClassId=0, ClassName=detection['class'], Confidence=detection['confidence'], BBox= detection['bbox'], Format="xywh_normalized"))
#             ROIVectorsM1.add(id=id, embedding_values=[float(num_str) for num_str in detection['roi_embedding']])
        
#         attributes_dict = {}
#         attributes = item.get("attributes", {})
#         for key, value in attributes.items():
#             attributes_dict[key] = StringElement(value)

#         image_embeddings = item.get("image_embedding", {})
#         for value in image_embeddings:
#             ImageVectorsM1.add(Embedding(value))

#         data_point = {
#             'ImageUri':StringElement(item["image_url"]),
#             'ImageId': StringElement(item["inputs"][0]),
#             'TimeOfCapture': TimeStampElement(item["capture_time"]),
#             f'Annotations {model_name}': AnnotationsV1,
#             f'ImageVectors {model_name}': ImageVectorsM1,
#             f'ROIVectors {model_name}': ROIVectorsM1,
#         }

#         merged_dict = {**data_point, **attributes_dict}

#         test_df.append(merged_dict)
        

# pd_data_frame = pd.DataFrame(test_df)
# # data_frame_extractor(pd_data_frame).to_csv("xyz_t.csv",index=False) # converted csv file 

# test_df1 = []
# with open(ds_json_file1, 'r') as json_file:
#     # Load JSON data
#     json_data = json.load(json_file)
    
#     # Process the JSON data
#     transformed_data = []
#     for item in json_data:
#         AnnotationsV2 = ImageDetectionObject()
#         ROIVectorsM2 = ROIEmbedding()
#         ImageVectorsM2 = ImageEmbedding()
#         for index, detection in enumerate(item["outputs"][0]["detections"]):
#             id = index+1
#             AnnotationsV2.add(ObjectDetection(Id=id, ClassId=0, ClassName=detection['class'], Confidence=detection['confidence'], BBox= detection['bbox'], Format="xywh_normalized"))
#             ROIVectorsM2.add(id=id, embedding_values=[float(num_str) for num_str in detection['roi_embedding']])
        
#         attributes_dict = {}
#         attributes = item.get("attributes", {})
#         for key, value in attributes.items():
#             attributes_dict[key] = StringElement(value)

#         image_embeddings = item.get("image_embedding", {})
#         for value in image_embeddings:
#             ImageVectorsM2.add(Embedding(value))

#         data_point = {
#             'ImageUri':StringElement(item["image_url"]),
#             'ImageId': StringElement(item["inputs"][0]),
#             'TimeOfCapture': TimeStampElement(item["capture_time"]),
#             f'Annotations {model_name1}': AnnotationsV2,
#             f'ImageVectors {model_name1}': ImageVectorsM2,
#             f'ROIVectors {model_name1}': ROIVectorsM2,
#         }

#         merged_dict = {**data_point, **attributes_dict}

#         test_df1.append(merged_dict)
        

# pd_data_frame1 = pd.DataFrame(test_df1)
# # pd_data_frame1.to_csv("xyz_f.csv",index=False)


# #create schema object of RagaSchema instance
# schema = RagaSchema()
# schema.add("ImageUri", ImageUriSchemaElement(), pd_data_frame)
# schema.add("ImageId", PredictionSchemaElement(), pd_data_frame)
# schema.add("TimeOfCapture", TimeOfCaptureSchemaElement(), pd_data_frame)
# schema.add("Reflection", AttributeSchemaElement(), pd_data_frame)
# schema.add("Overlap", AttributeSchemaElement(), pd_data_frame)
# schema.add("CameraAngle", AttributeSchemaElement(), pd_data_frame)
# schema.add(f"Annotations {model_name}", InferenceSchemaElement(model=model_name), pd_data_frame)
# schema.add(f"ImageVectors {model_name}", ImageEmbeddingSchemaElement(model=model_name), pd_data_frame)
# schema.add(f"ROIVectors {model_name}", RoiEmbeddingSchemaElement(model=model_name), pd_data_frame)

# schema1 = RagaSchema()
# schema1.add("ImageUri", ImageUriSchemaElement(), pd_data_frame1)
# schema1.add("ImageId", PredictionSchemaElement(), pd_data_frame1)
# schema1.add("TimeOfCapture", TimeOfCaptureSchemaElement(), pd_data_frame1)
# schema1.add("Reflection", AttributeSchemaElement(), pd_data_frame1)
# schema1.add("Overlap", AttributeSchemaElement(), pd_data_frame1)
# schema1.add("CameraAngle", AttributeSchemaElement(), pd_data_frame1)
# schema1.add(f"Annotations {model_name1}", InferenceSchemaElement(model=model_name1), pd_data_frame1)
# schema1.add(f"ImageVectors {model_name1}", ImageEmbeddingSchemaElement(model=model_name1), pd_data_frame1)
# schema1.add(f"ROIVectors {model_name1}", RoiEmbeddingSchemaElement(model=model_name1), pd_data_frame1)

project_name = "testingProject" # Project Name
run_name= "Test_Drift_NuScene_8Aug23V2" # Experiment Name
dataset_name_t = "train-dataset-7-aug-v2" # Dataset Name for train
dataset_name_f = "field-dataset-7-aug-v2" # Dataset Name for feild
#train_embed_col_name = f'ImageVectors{model_name}' #Train dataset embedding column name
#field_embed_col_name = f'ImageVectors{model_name1}' #Field dataset embedding column name




#create test_session object of TestSession instance
test_session = TestSession(project_name=project_name,run_name=run_name)



#create test_ds object of Train Dataset instance
#test_ds1 = Dataset(test_session=test_session, name=dataset_name_t)

#load schema and pandas data frame of train dataset

#test_ds1.load(pd_data_frame, schema)



#create test_ds object of Feild Dataset instance
#test_ds2 = Dataset(test_session=test_session, name=dataset_name_f)

#load schema and pandas data frame of Feild Dataset
#test_ds2.load(pd_data_frame1, schema1)


# #add payload into test_session object
# test_session.add(data_drift_detection)

testName = StringElement("test-labelled-Aug-8_v2")
train_dataset_name = StringElement(dataset_name_t)
field_dataset_name = StringElement(dataset_name_f)
train_embed_col_name = StringElement("ImageEmbedding")  #for train col in image level
field_embed_col_name = StringElement("ImageEmbedding")  #for field col in image level
level = StringElement("image")

# train_embed_col_name = StringElement("ROIVectors Train")      #for train col in roi level
# field_embed_col_name = StringElement("ROIVectors Field")      #for field col in roi level
# level = StringElement("roi")
aggregation_level = AggregationLevelElement()
# aggregation_level.add(StringElement("Reflection"))
# aggregation_level.add(StringElement("Overlap"))
# aggregation_level.add(StringElement("CameraAngle"))
rules = DriftDetectionRules()
rules.add(type=StringElement("anomaly_detection"), dist_metric=StringElement("Euclidian"), _class = StringElement("ALL"), threshold = FloatElement(0.5))

edge_case_detection = data_drift_detection(test_session, testName=testName, train_dataset_name=train_dataset_name, field_dataset_name=field_dataset_name, train_embed_col_name=train_embed_col_name, field_embed_col_name = field_embed_col_name , level = level, aggregation_level=aggregation_level, rules = rules)

# print(edge_case_detection)

# #add payload into test_session object
test_session.add(edge_case_detection)

# #run added ab test model payload
test_session.run()
