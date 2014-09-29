
$(function() {


//Geography: lookup geonameid
	$( "#addGeoNameID" ).autocomplete({
		delay: 2000,
		minLength: 3,
        position: { my : "right top", at: "right bottom" },
		source: function( request, response ) {
			$.ajax({
				url: "/contribute/geosearch",
				dataType: "json",
				data: {
					"term": request.term,
					"c": $('#co').val(),
					"p": $('#pr').val()
				},
				success: function(data){
					response( $.map( data.terms, function( item ) {
						return {
							label: item.term,
							value: item.id,
							latitude: item.latitude,
							longitude: item.longitude,
							name: item.name
						}
					}));
				}
			});
		},
		open: function() {
			$( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" )
            },
		close: function() {
			$( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
		},
		select: function( event, ui ) {
			$("#addGeoNameID").val("");
			$("#geographyChecklist").append(
				"<dt><input type='checkbox' name='geonameid' value='" + ui.item.value +"' checked='checked' /> &nbsp;" + ui.item.label +"</dt>"
			);
			var gmapvalues = ui.item.latitude +'|'+ui.item.longitude+'|'+ui.item.name
			$("#geoLatLng").append(gmapvalues +";");
			gMapInitialize();
			//window.gMapInitialize = function(ui.item.latlong);
			return false;
		}
	});


});