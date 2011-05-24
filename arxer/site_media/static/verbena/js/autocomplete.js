document.getElementById("id_title").onkeyup = function () {
	var e = document.getElementById("id_slug");
	if (!e._changed) { 
		e.value =	URLify(document.getElementById("id_title").value, 75); 
	}
}


