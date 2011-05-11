/**
 * The search bar scripts. These are used to change the value upon clicking and
 * to use the autocomplete function.
 * REQUIRES: jQuery, jQuery Autocomplete
 */
$('#bar_q').click(function () {
	$('#bar_q').val('');
});	

$(function() {
	var cache = {},
			lastXhr;
	$('#bar_q').autocomplete({
		minLength: 3, // because we will use "name__contains"
		source: "/autocomplete",
		//select: function( event, ui )
	});
});
