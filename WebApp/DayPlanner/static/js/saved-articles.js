$(document).ready(function() {
    'use strict';
    var table = $('#dataTables').DataTable({
        responsive: true

    });
    $('#dataTables tbody').on( 'click', 'tr', function () {
        if ($(this).hasClass('active') ) {
            $(this).removeClass('active');

            $("#modify-article").addClass('disabled');
            $("#delete-article").addClass('disabled');
            
        }
        else {
            // table.$('tr.active').removeAttr('id');
            table.$('tr.active').removeClass('active');
            $(this).addClass('active');
            // $(this).attr('id', 'active');

            $("#modify-article").removeClass('disabled');
            $("#delete-article").removeClass('disabled');

            var article_id = table.row( this ).data()[0];
            $("#modify-article").attr('href',"/app/saved-articles/modify/" + article_id);
            $("#delete-article").attr('href',"/app/saved-articles/delete/" + article_id);
        }
    });

});