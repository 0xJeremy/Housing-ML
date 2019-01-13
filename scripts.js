var clear_form = document.getElementById("clear_form");
var calculate_price = document.getElementById("calculate_price");

var model;
window.onload = async function load_model() {
	model = await tf.loadModel('model.json');
	console.log("Model Loaded");
}

function add_commas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

clear_form.onclick = function() {
	document.getElementById("beds").value = "";
	document.getElementById("baths").value = "";
	document.getElementById("sqfootage").value = "";
	document.getElementById("zipcode").value = "";
	document.getElementById("avgprice").value = "";
	document.getElementById("result").innerHTML = "";
}

calculate_price.onclick = function() {
	num_beds = parseFloat(document.getElementById("beds").value);
	num_baths = parseFloat(document.getElementById("baths").value);
	square_footage = parseFloat(document.getElementById("sqfootage").value);
	zipcode = parseFloat(document.getElementById("zipcode").value);
	avg_price = parseFloat(document.getElementById("avgprice").value);
	if(num_beds && num_baths && square_footage && zipcode && avg_price) {
		price = predict_price();
		document.getElementById("result").innerHTML = "</br></br><div class=\"text-center alert alert-success\" role=\"alert\">Calculated Price: $" + add_commas(price) + "</div>";	
	}
	else {
		document.getElementById("result").innerHTML = "</br></br><div class=\"text-center alert alert-danger\" role=\"alert\">Error: Missing Information</div>";
	}
}

function predict_price() {
	prediction_tensor = tf.tensor2d([num_beds, num_baths, square_footage, zipcode], [1, 4]);
	const prediction = model.predict(prediction_tensor);
	value = prediction.dataSync();
	return parseInt(value[0], 10);
}

// https://js.tensorflow.org/tutorials/import-saved-model.html
// https://js.tensorflow.org/tutorials/import-keras.html
// run with "python -m http.server"