var clear_form = document.getElementById("clear_form");
var calculate_price = document.getElementById("calculate_price");

clear_form.onclick = function() {
	document.getElementById("beds").value = "";
	document.getElementById("baths").value = "";
	document.getElementById("sqfootage").value = "";
	document.getElementById("zipcode").value = "";
	document.getElementById("avgprice").value = "";
}

calculate_price.onclick = function() {
	num_beds = document.getElementById("beds").value;
	num_baths = document.getElementById("baths").value;
	square_footage = document.getElementById("sqfootage").value;
	zipcode = document.getElementById("zipcode").value;
	avg_price = document.getElementById("avgprice").value;
}

// https://js.tensorflow.org/tutorials/import-saved-model.html
// https://js.tensorflow.org/tutorials/import-keras.html