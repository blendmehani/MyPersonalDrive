    $(document).ready(function () {
        var t = $('#recycle_bin_table').DataTable({
            "columnDefs": [{
                "searchable": true,
                targets: 2,
            }, {
                "searchable": false,
                targets: [4, 5, 6],
            }, {
                "searchable": false,
                "orderable": false,
                targets: [0, "no-sort"],
            }],
            "order": [[6, 'asc']],

        });

        t.on('order.dt search.dt', function () {
            t.column(0, {search: 'applied', order: 'applied'}).nodes().each(function (cell, i) {
                cell.innerHTML = i + 1;
            });
        }).draw();
    });

    document.getElementById('search_bar').style.display = 'none'