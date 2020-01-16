#Preparing workspace
========
Annotating images
    unzip file images.zip and follow directory tree:
        images
            - test
            - train
Creating Label Map
    label_map.pbtxt

Creating TensorFlow Records
        - Converting *.xml to *.csv 
            - Run file xml_to_csv.py
        - Converting from *.csv to *.record 
            - Run file generate_tfrecord.py

Configuring a Training Pipeline
    - pipeline.config
    
Training the Model 
    - Run file train.py

Monitor Training Job Progress using TensorBoard
    - Open a new Anaconda/Command Prompt
        - activate tensorflow gpu
        - tensorboard --logdir=training\
        
Exporting a Trained Inference Graph
   - Run export_inference_graph.py
   
If you want to test detection with 
    - image: Run object_detection_image.py
    - video: Run object_detection_video.py
    - webcam: Run object_detection_webcam.py
