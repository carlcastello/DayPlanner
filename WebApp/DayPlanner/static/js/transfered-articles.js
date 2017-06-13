
$(document).ready(function() {
    'use strict';
    var table = $('#dataTables').DataTable({
        responsive: true,
        "columnDefs": [
            {
                "targets": [6],
                "searchable": false
            }
        ]

    });
    
    var datepickerDefaults = {
        showTodayButton: true,
        showClear: true
    };

    yadcf.init(table, [{
        column_number: 0,
        filter_container_id: 'search_0',
        filter_type: "multi_select",
        select_type: 'select2', 
        filter_default_label: "Article Number"
    },{
        column_number: 1,
        filter_container_id: 'search_1',
        filter_type: "multi_select",
        select_type: 'select2', 
        filter_default_label: "Article Name" 
    },{
        column_number: 2,
        filter_container_id: 'search_2',
        filter_type: "multi_select",
        select_type: 'select2', 
        filter_default_label: "User ID" 
    },{
        column_number: 3,
        filter_container_id: 'search_3',
        filter_type: "multi_select",
        select_type: 'select2', 
        filter_default_label: "Location" 
    },{
        column_number: 4,
        filter_container_id: 'search_4',
        filter_type: "multi_select",
        select_type: 'select2', 
        filter_default_label: "Quantity"
    }],
    {
        cumulative_filtering: true
    });

});

$(document).ready(function() {
    var table = $('#dataTables').DataTable()

    var counterChecked = 0;
    $('#dataTables tbody').on( 'click', 'tr', function () {
        if ($(this).hasClass('active') ) {
            counterChecked--;
        }
        else {
            counterChecked++;
        }
        if(counterChecked > 0){
            $("#confirm-article").removeClass('disabled');
        } else {
            $("#confirm-article").addClass('disabled');
        }
        $(this).toggleClass('active');

    });

    $('#confirm-article').click( function () {
        var Things = table.rows('.active').data();
        var strings = ""
        for (var i = Things.length - 1; i >= 0; i--) {
            strings = strings +"&"+ Things[i][6]
        }
        window.location.href = "/app/transfered-articles/confirm/" + strings;
    });

 
});

$(document).ready(function () {
    var datepickerDefaults = {
        showTodayButton: true,
        showClear: true
    };
    $('#dataTables').dataTable().yadcf([
        {
            column_number: 5,
            filter_container_id: 'search_5',
            filter_type: "range_date",
            datepicker_type: 'bootstrap-datetimepicker', 
            date_format: 'YYYY-MM-DD', 
            select_type: 'select2', 
            filter_plugin_options: datepickerDefaults
        }
    ])
});
