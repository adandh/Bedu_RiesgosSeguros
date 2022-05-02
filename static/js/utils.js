/**
 * Funciones auxiliares 
 */


$("#atras").click(function() {
  goBack();
});
function goBack() {
    window.history.back();
}


$('#submit_button').click(function(){	
  $("#procesando").show();
  $("#atras").prop( "disabled", true );  
  $("#submit_button").prop( "disabled", true );
	$("#form").submit();	

});


/*$('#submit_button').click(function(){
	var filePath = fileInput.value;
    var allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
    if(!allowedExtensions.exec(filePath)){
        alert('Please upload file having extensions .jpeg/.jpg/.png/.gif only.');
        fileInput.value = '';
        return false;
    }

    else{
		$("#form").submit();
	}
	//return true;
});*/

$('#submit_button_global').click(function(){
    $(":input").each(function(){
			console.log( $(this));
			$("#fGlobal").append($(this)); // This is the jquery object of the input, do what you will
		});
    $("#fGlobal").submit();
});


  $(document).ready(function(){
    $('select').formSelect();
    $("#procesando").hide();
  });


/*  $(document).ready(function(){
    $('.datepicker').datepicker();
  });
*/

 document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.datepicker');
    var options = {'format': 'yyyy-mm-dd'}
    var instances = M.Datepicker.init(elems, options);
  });

  $(document).ready(function(){    
  	$(".dropdown-trigger").dropdown(

                                      {     alignment:'right',
                                            autoTrigger:false,
                                            inDuration: 1000,
                                            outDuration: 250,
                                            coverTrigger: false,
                                            hover: true, // Activate on hover
                                            belowOrigin: false, // Displays dropdown below the button                                            
                                            alignment: 'left' // Displays dropdown with edge aligned to the left of button
                                          }
                                    );
  });