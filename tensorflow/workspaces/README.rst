#Preparing workspace
========
# Annotating images
    unzip file images.zip and follow directory tree:
        images
            - test
            - train
# Creating Label Map
item {
    id: 1
    name: 'AphId'
}
item {
    id: 2
    name: 'BeanLeafBeetle'
}
item {
    id: 3
    name: 'CabbageLooper'
}
item {
    id: 4
    name: 'ColoradoPotatoBeetle'
}

item {
    id: 5
    name: 'Cutworm'
}
item {
    id: 6
    name: 'SquashBug'
}

# Creating TensorFlow Records

    Converting *.xml to *.csv (run file generate_tfrecord.py)

    Converting from *.csv to *.record (run file xml_to_csv.py)

# Configuring a Training Pipeline

# Training the Model (run file train.py)

# Monitor Training Job Progress using TensorBoard

# Exporting a Trained Inference Graph
