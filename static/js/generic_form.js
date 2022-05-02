
/**
 * Selector de fechas
 */
$( document ).ready(function() {
    $(this).scrollTop(0);
    console.log( "Ready insert-edit");
    $('#div-date').hide();
    initDates();

});



function initDates () {

 var container = $('.bootstrap-iso form').length > 0 ? $('.bootstrap-iso form').parent() : "body";
    var options = {
        format: 'yyyy-mm-dd',
        container: container,
        todayHighlight: true,
        autoclose: true,
    };

    $.each( $("input[name^='fecha']"), function () {
          $(this).datepicker(options);
            //alert( $(this) );
        });


}
