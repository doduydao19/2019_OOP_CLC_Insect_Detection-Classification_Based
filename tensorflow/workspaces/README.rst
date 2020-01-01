#Preparing workspace
========
#Annotating images

- Once you have finished annotating your image dataset, it is a general convention to use only part of it for training, and the rest is used for testing purposes. Typically, the ratio is 90%/10%.

#Creating Label Map

- TensorFlow requires a label map, which namely maps each of the used labels to an integer values. This label map is used both by the training and detection processes.

#Creating TensorFlow Records

- Generated our annotations and split our dataset into the desired training and testing subsets, it is time to convert our annotations into the so called TFRecord format.

    Converting *.xml to *.csv (run file generate_tfrecord.py)

    Converting from *.csv to *.record (run file xml_to_csv.py)

#Configuring a Training Pipeline

#Training the Model (run file train.py)

#Monitor Training Job Progress using TensorBoard

Open a new Anaconda/Command Prompt

- activate tensorflow_gpu

- tensorboard --logdir=training\

TensorBoard 1.6.0 at http://YOUR-PC:6006 (Press CTRL+C to quit)

#Exporting a Trained Inference Graph

Open a new Anaconda/Command Prompt
- activate tensorflow_gpu

- python export_inference_graph.py --input_type image_tensor --pipeline_config_path training/ssd_inception_v2_coco.config --trained_checkpoint_prefix training/model.ckpt-13302 --output_directory trained-inference-graphs/output_inference_graph_v1.pb
