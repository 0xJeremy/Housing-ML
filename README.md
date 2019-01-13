# Housing AI

### Predicting Prices

All price prediction is done in a web browser. Use a web server to serve the page: ex. `python -m http.server [port]`. The page will be loaded to `localhost:[port]`.
To modify the trained model used to predict prices, replace `model.json` with a Keras trained model. See TensorFlow.js for more information.
Note: The file containing the weights of the associated json model must also be included when using a new model.

### Training new Models

The TensorFlow models were trained in python before being ported to TensorFlow.js. To retrain a model, use the program found in the `python` folder.
This code can be modified and reused to train with new datasets. The trained model can be saved as `model.json` and used to make predictions (see above for more details).