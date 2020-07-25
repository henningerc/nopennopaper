    function clickDeleteHead(event) {
        var d_out = {'head_id': event.target.getAttribute("head_id")};
        console.log(d_out);
        $.post('aj_delete_head', d_out, function(d_in){
            if(d_in.deleted){
                $('tr#' + d_in.id).remove()
            }
        });
        event.preventDefault();
    }

    function clickDeleteAttribute(event) {
        var d_out = {'att_id': event.target.getAttribute("att_id")};
        console.log(d_out);
        $.post('aj_delete_attribute', d_out, function(d_in){
            if(d_in.deleted){
                $('tr#' + d_in.id).remove()
            }
        });
        event.preventDefault();
    }

    function submitAttributeForm(event) {
        var id = event.target.getAttribute("att_id");
        d_out = {'att_id': id,
                'title': $('input.title[att_id="' + id + '"]').val(),
                'description': $('input.description[att_id="' + id + '"]').val()}
        $.post('aj_set_attribute', d_out, function(d_in){
            if(id=='new_attribute') {
                $('tr#new_attribute').attr('id', d_in.id);
            }
            var row = $('tr#' + d_in.id);
            row.children('td.title').text(d_in.title);
            row.children('td.description').text(d_in.description);
            row.children('td.buttons').html('');
            row.on('click', showAttributeForm);
        })
    }

    function submitHeadForm(event) {
        var id = event.target.getAttribute("head_id");
        d_out = {'head_id': id,
                'title': $('input.title[head_id="' + id + '"]').val(),
                'description': $('input.description[head_id="' + id + '"]').val(),
                'order': $('input.order[head_id="' + id + '"]').val(),
                'standard': ($('input.standard[head_id="' + id + '"]').is(':checked')? true: false)};
        if(id=='new_header') {
            id = 'new';
            d_out.head_id = id;
        }

        $.post('aj_set_head', d_out, function(d_in){
            if(id=='new') {
                $('tr#new_header').attr('id', d_in.id);
            }
            $('tr#' + d_in.id + ' td.title').text(d_in.title);
            $('tr#' + d_in.id + ' td.description').text(d_in.description);
            $('tr#' + d_in.id + ' td.order').text(d_in.order);
            $('tr#' + d_in.id + ' td.standard').html(d_in.standard?'&check;':'x');
            $('tr#' + d_in.id + ' td.buttons').text('');
            $('tr#' + d_in.id).on('click', showHeadForm);
        });
    }

    function showAttributeForm(event) {
        var req_item = this;
        $.post('aj_get_attribute', {'attribute_id': req_item.id}, function(d_in){
            var row = $('tr#' + d_in.id);
            row.off('click');
            row.children('td.title').html('<input type="text" class="title" att_id="' + d_in.id + '" value="' + d_in.title + '" />');
            row.children('td.description').html('<input type="text" class="description" att_id="' + d_in.id + '" value="' + d_in.description + '" />')
            row.children('td.buttons').html('<a href="javascript:void(0)" class="submit" att_id="' + d_in.id + '">(&check;)</a>'
                    + '<a href="javascript:void(0)" class="delete" att_id="' + d_in.id + '">(X)</a>');
            $('a.submit[att_id="' + d_in.id + '"]').on('click', submitAttributeForm);
            $('a.delete[att_id="' + d_in.id + '"]').on('click', clickDeleteAttribute);
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
                .html('<a href="javascript:void(0)" class="submit" head_id="' + data.id + '">(&check;)</a>'
                    + '<a href="javascript:void(0)" class="delete" head_id="' + data.id + '">(X)</a');
            $('a.submit[head_id="' + data.id + '"]').on('click', submitHeadForm);
            $('a.delete[head_id="' + data.id + '"]').on('click', clickDeleteHead);
        });
    }

    $('a#new_head').on('click', function(event){
        // TODO: Doppelte neue verhindern oder kennzeichnen
        var new_tr = '<tr id="new_header" class="editable head_value">'
            + '<td class="title"><input type="text" class="title" head_id="new_header" value="" /></td>'
            + '<td class="description"><input type="text" class="description" head_id="new_header" value="" /></td>'
            + '<td class="order"><input type="number" class="order" head_id="new_header" value="" /></td>'
            + '<td class="standard"><input type="checkbox" class="standard" head_id="new_header" /></td>'
            + '<td class="buttons"><a href="javascript:void(0)" class="submit" head_id="new_header">(&check;)</a></td>'
            + '</tr>';
        $('table#headers').append(new_tr);
        $('a.submit[head_id="new_header"]').on('click', submitHeadForm);
    });

    $('a#new_attribute').on('click', function(event){
        // TODO: Doppelte neue verhindern oder kennzeichnen
        var new_tr = '<tr id="new_attribute" class="editable attribute">'
            + '<td class="title"><input type="text" class="title" att_id="new_attribute" value="" /></td>'
            + '<td class="description"><input type="text" class="description" att_id="new_attribute" value="" /></td>'
            + '<td class="buttons"><a href="javascript:void(0)" class="submit" att_id="new_attribute">(&check;)</a></td>'
            + '</tr>';
        $('table#attributes').append(new_tr);
        $('a.submit[att_id="new_attribute"]').on('click', submitAttributeForm);
    });

    $('tr.head_value').on('click', showHeadForm);
    $('tr.attribute').on('click', showAttributeForm);
    // TODO: SameSite-Probleme in der Java-Console zu sehen
