export function createLoader(loaderText) {
	console.log("in loader");
	let contentString = "";

	if (loaderText) {
		contentString = "<div class=\"loader__text\">" + loaderText + "</div>";
	}

	let modal = document.createElement('div');
	modal.className = "loader";
	modal.innerHTML = "<div class=\"loader__content\">" +
			contentString +
			"<br><img src=\"https://res.cloudinary.com/dzhpku2a7/image/upload/v1604934493/helpers/loader.gif\"/>" +
		"</div>";

	document.body.append(modal);
}


export function destroyLoader() {
	document.querySelector(".loader").remove();
}
