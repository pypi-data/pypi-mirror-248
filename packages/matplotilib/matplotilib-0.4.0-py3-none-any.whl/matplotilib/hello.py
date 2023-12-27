import nbformat

def hello():
    notebook_content = r"""
    {
      "cells": [
        {
          "cell_type": "code",
          "execution_count": null,
          "id": "daec8c3b",
          "metadata": {
            "id": "daec8c3b"
          },
          "outputs": [],
          "source": [
            "import os\n",
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "from tensorflow.keras.preprocessing.image import ImageDataGenerator\n",
            "from tensorflow.keras.models import Sequential\n",
            "from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout\n",
            "from tensorflow.keras.regularizers import l2\n",
            "from sklearn.metrics import confusion_matrix, classification_report"
          ]
        },
        {
          "cell_type": "code",
          "execution_count": null,
          "id": "36478bba",
          "metadata": {
            "id": "36478bba"
          },
          "outputs": [],
          "source": [
            "# Set the file path where images are stored\n",
            "data_dir = '/Users/kalpeshprabhakar/Desktop/E/Tomato Dataset'\n"
          ]
        },
        {
          "cell_type": "code",
          "execution_count": null,
          "id": "03e54267",
          "metadata": {
            "id": "03e54267"
          },
          "outputs": [],
          "source": [
            "# Image Augmentation\n",
            "datagen = ImageDataGenerator(\n",
            "    rescale=1./255,\n",
            "    shear_range=0.2,\n",
            "    zoom_range=0.2,\n",
            "    horizontal_flip=True,\n",
            "    validation_split=0.2  # Adjust the validation split as needed\n",
            ")"
          ]
        },
        {
          "cell_type": "code",
          "execution_count": null,
          "id": "759143a2",
          "metadata": {
            "id": "759143a2"
          },
          "outputs": [],
          "source": [
            "#Building the model\n",
            "\n",
            "model = Sequential()\n",
            "model.add(Conv2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu', strides=(1, 1), kernel_regularizer=l2(0.01)))\n",
            "model.add(MaxPooling2D(pool_size=(2, 2)))\n",
            "model.add(Dropout(0.25))  # Adding dropout after MaxPooling\n",
            "model.add(Conv2D(64, (3, 3), activation='relu', strides=(1, 1), kernel_regularizer=l2(0.01)))\n",
            "model.add(MaxPooling2D(pool_size=(2, 2)))\n",
            "model.add(Dropout(0.25))  # Adding dropout after MaxPooling\n",
            "model.add(Flatten())\n",
            "model.add(Dense(units=128, activation='relu', kernel_regularizer=l2(0.01)))\n",
            "model.add(Dropout(0.5))  # Adding dropout before the output layer\n",
            "model.add(Dense(units=10, activation='softmax'))  # For multi-class classification\n",
            "\n",
            "# Model Summary\n",
            "model.summary()"
          ]
        },
        {
          "cell_type": "code",
          "execution_count": null,
          "id": "0b7b77f3",
          "metadata": {
            "id": "0b7b77f3"
          },
          "outputs": [],
          "source": [
            "# Model Compilation\n",
            "model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])\n",
            "\n",
            "# Model Training\n",
            "batch_size = 32\n",
            "train_set = datagen.flow_from_directory(\n",
            "    data_dir,\n",
            "    target_size=(64, 64),\n",
            "    batch_size=batch_size,\n",
            "    class_mode='categorical',\n",
            "    subset='training'  # Use training subset\n",
            ")\n",
            "\n",
            "val_set = datagen.flow_from_directory(\n",
            "    data_dir,\n",
            "    target_size=(64, 64),\n",
            "    batch_size=batch_size,\n",
            "    class_mode='categorical',\n",
            "    subset='validation'  # Use validation subset\n",
            ")\n",
            "\n",
            "history = model.fit(train_set, epochs=10, validation_data=val_set)"
          ]
        },
        {
          "cell_type": "code",
          "execution_count": null,
          "id": "465b8bd0",
          "metadata": {
            "id": "465b8bd0"
          },
          "outputs": [],
          "source": [
            "# Model Testing\n",
            "test_set = datagen.flow_from_directory(\n",
            "    data_dir,\n",
            "    target_size=(64, 64),\n",
            "    batch_size=batch_size,\n",
            "    class_mode='categorical',\n",
            "    shuffle=False  # Do not shuffle for confusion matrix and classification report\n",
            ")\n"
          ]
        },
        {
          "cell_type": "code",
          "execution_count": null,
          "id": "b5caf3f4",
          "metadata": {
            "id": "b5caf3f4"
          },
          "outputs": [],
          "source": [
            "# Assuming your model has been compiled for categorical_crossentropy\n",
            "predictions = model.predict(test_set)\n",
            "\n",
            "\n",
            "# Get the predicted class for each instance\n",
            "y_pred = np.argmax(predictions, axis=1)\n",
            "\n",
            "# Confusion Matrix\n",
            "cm = confusion_matrix(test_set.classes, y_pred)\n",
            "print(\"Confusion Matrix:\")\n",
            "print(cm)\n"
          ]
        },
        {
          "cell_type": "code",
          "execution_count": null,
          "id": "82cea12b",
          "metadata": {
            "id": "82cea12b"
          },
          "outputs": [],
          "source": [
            "# Assuming your model has been compiled for categorical_crossentropy or binary_crossentropy\n",
            "test_loss, test_accuracy = model.evaluate(test_set)\n",
            "\n",
            "# Print Testing Accuracy\n",
            "print(\"Testing Accuracy: {:.2%}\".format(test_accuracy))"
          ]
        },
        {
          "cell_type": "code",
          "execution_count": null,
          "id": "cdb6d51e",
          "metadata": {
            "id": "cdb6d51e"
          },
          "outputs": [],
          "source": [
            "# Classification Report\n",
            "print(\"\\nClassification Report:\")\n",
            "print(classification_report(test_set.classes, y_pred))\n"
          ]
        },
        {
          "cell_type": "code",
          "execution_count": null,
          "id": "1beaf9a7",
          "metadata": {
            "id": "1beaf9a7"
          },
          "outputs": [],
          "source": [
            "# Plot Training History\n",
            "plt.plot(history.history['accuracy'], label='Training Accuracy')\n",
            "plt.plot(history.history['val_accuracy'], label='Validation Accuracy')\n",
            "plt.xlabel('Epochs')\n",
            "plt.ylabel('Accuracy')\n",
            "plt.legend()\n",
            "plt.show()\n",
            "\n",
            "plt.plot(history.history['loss'], label='Training Loss')\n",
            "plt.plot(history.history['val_loss'], label='Validation Loss')\n",
            "plt.xlabel('Epochs')\n",
            "plt.ylabel('Loss')\n",
            "plt.legend()\n",
            "plt.show()"
          ]
        }
      ],
      "metadata": {
        "kernelspec": {
          "display_name": "Python 3",
          "name": "python3"
        },
        "language_info": {
          "codemirror_mode": {
            "name": "ipython",
            "version": 3
          },
          "file_extension": ".py",
          "mimetype": "text/x-python",
          "name": "python",
          "nbconvert_exporter": "python",
          "pygments_lexer": "ipython3",
          "version": "3.11.4"
        },
        "colab": {
          "provenance": [],
          "gpuType": "T4"
        },
        "accelerator": "GPU"
      },
      "nbformat": 4,
      "nbformat_minor": 5
    }
    """


    # Save the notebook content to a file
    notebook_path = 'EndSem.ipynb'
    with open(notebook_path, 'w', encoding='utf-8') as notebook_file:
        notebook_file.write(notebook_content)

    print(f"Notebook created at: {notebook_path}")
    print(r"""import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, LSTM, Dense

# Load and preprocess the data
def preprocess_data(images, labels):
    data = []
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)

    for img_path in images:
        img = load_img(img_path, target_size=(64, 64))  # Adjust the target size as needed
        img_array = img_to_array(img) / 255.0  # Normalize pixel values to be between 0 and 1
        data.append(img_array)

    return np.array(data), to_categorical(labels_encoded)

# Preprocess the data
X, y = preprocess_data(images, labels)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Parameters
sequence_length = X_train.shape[1]  # Length of the sequences (number of time steps)
height, width, channels = X_train.shape[2:]  # Assuming input shape (height, width, channels)
embedding_dim = 64  # Size of the dense embedding
lstm_units = 100  # Number of LSTM units
num_classes = len(np.unique(labels))  # Number of classes

# Create a ConvLSTM model
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(height, width, channels)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(LSTM(units=lstm_units))
model.add(Dense(units=num_classes, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Display the model summary
model.summary()

# Train the model
batch_size = 32
epochs = 10

history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2)

# Evaluate the model on the testing set
test_loss, test_accuracy = model.evaluate(X_test, y_test)

# Print the testing results
print(f"\nTesting Accuracy: {test_accuracy * 100:.2f}%")
print(f"Testing Loss: {test_loss:.4f}")

# Plot training history
import matplotlib.pyplot as plt

def plot_history(history):
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend(['Train', 'Validation'], loc='upper left')

    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(['Train', 'Validation'], loc='upper left')

    plt.tight_layout()
    plt.show()
    
# Plot the training history
plot_history(history)""")

# Uncomment the line below if you want to create the notebook on function call
# create_notebook()
