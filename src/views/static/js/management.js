    // TODO: Löschen-Button so einrichten, dass er von sich aus nicht submitted
    function clickDelete(event) {
        var d_out = {'head_id': event.target.getAttribute("head_id")};
        console.log(d_out);
        $.post('aj_delete_head', d_out, function(d_in){
            if(d_in.deleted){
                $('tr#' + d_in.id).remove()
            }
        });
        event.preventDefault();
    }

    function submitHeadForm(event) {
        var id = event.target.getAttribute("head_id");
        console.log(id);
        d_out = {'head_id': id,
                'title': $('input.title[head_id="' + id + '"]').val(),
                'description': $('input.description[head_id="' + id + '"]').val(),
                'order': $('input.order[head_id="' + id + '"]').val(),
                'standard': ($('input.standard[head_id="' + id + '"]').is(':checked')? true: false)};
        if(id=='new_header') {
            id = 'new';
            d_out.head_id = id;
        }
        console.log(d_out);

        $.post('aj_set_head', d_out, function(d_in){
            if(id=='new') {
                $('tr#new_header').attr('id', d_in.id);
            }
            $('tr#' + d_in.id + ' td.title').text(d_in.title);
            $('tr#' + d_in.id + ' td.description').text(d_in.description);
            $('tr#' + d_in.id + ' td.order').text(d_in.order);
            $('tr#' + d_in.id + ' td.standard').text(d_in.standard);
            $('tr#' + d_in.id + ' td.buttons').text('');
            $('tr#' + d_in.id).on('click', showHeadForm);

        });
    }

    function showHeadForm(event) {
        var req_item = this;
        $.post('aj_get_head', {'head_id': req_item.id}, function(data){
            console.log(data);
            $('tr#' + data.id).off('click');
            // TODO: Sollten eine KeyDown-Methode bekommen
            $('tr#' + data.id + ' td.title')
                .html('<input type="text" class="title" head_id="' + data.id + '" value="' + data.title + '" />');
            $('tr#' + data.id + ' td.description')
                .html('<input type="text" class="description" head_id="' + data.id + '" value="' + data.description + '" />');
            $('tr#' + data.id + ' td.order')
                .html('<input type="number" class="order" head_id="' + data.id + '" value="' + data.order + '" />');
            $('tr#' + data.id + ' td.standard')
                .html('<input type="checkbox" class="standard" head_id="' + data.id + '"' + (data.standard?' checked':'') + '/>');
            $('tr#' + data.id + ' td.buttons')
                .html('<button class="submit" head_id="' + data.id + '">speichern</button>'
                    + '<button class="delete" head_id="' + data.id + '">löschen</button>');
            $('button.submit[head_id="' + data.id + '"]').on('click', submitHeadForm);
            $('button.delete[head_id="' + data.id + '"]').on('click', clickDelete);
        });
    }

    $('a#new_head').on('click', function(event){
        // TODO: Doppelte neue verhindern oder kennzeichnen
        var new_tr = '<tr id="new_header" class="editable head_value">'
            + '<td class="title"><input type="text" class="title" head_id="new_header" value="" /></td>'
            + '<td class="description"><input type="text" class="description" head_id="new_header" value="" /></td>'
            + '<td class="order"><input type="number" class="order" head_id="new_header" value="" /></td>'
            + '<td class="standard"><input type="checkbox" class="standard" head_id="new_header" /></td>'
            + '<td class="buttons"><button class="submit" head_id="new_header">speichern</button></td>'
            + '</tr>';
        $('table#headers').append(new_tr);
        $('button.submit[head_id="new_header"]').on('click', submitHeadForm);
    });

    $('tr.editable').on('click', showHeadForm);
    // TODO: SameSite-Probleme in der Java-Console zu sehen
