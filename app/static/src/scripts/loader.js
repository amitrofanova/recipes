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
			"<img src=\"../static/images/loader.gif\"/>" +
		"</div>";

	// document.querySelector("main.container").append(modal);
	document.body.append(modal);
}


export function destroyLoader() {
	document.querySelector(".loader").remove();
}
