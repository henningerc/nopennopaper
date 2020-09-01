/**********************
** Helping functions **
**********************/
function createSelect(class_names, id_field, id, values, selected) {
    select = '<select class="' + class_names +'" ' + id_field + '="' + id + '">\n';
    for(v in values) {
        select += '<option value="' + values[v].id + '"' + (values[v].id==selected?' selected':'') + '>'
            + values[v].text + '</option>\n';
    }
    select += "</select>\n";
    return select;
}

function getButton(button, path_class, im_size) {
    var value;
    //TODO: Inneres anklickbar und weiß machen
    if(button=="checkmark")
        value = 'M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm4.3 7.61l-4.57 6a1 1 0 0 1-.79.39 1 1 0 0 1-.79-.' +
        '38l-2.44-3.11a1 1 0 0 1 1.58-1.23l1.63 2.08 3.78-5a1 1 0 1 1 1.6 1.22z" class="';
    if(button=="trash")
        value='M21 6h-5V4.33A2.42 2.42 0 0 0 13.5 2h-3A2.42 2.42 0 0 0 8 4.33V6H3a1 1 0 0 0 0 2h1v11a3 3 0 0' +
        ' 0 3 3h10a3 3 0 0 0 3-3V8h1a1 1 0 0 0 0-2zM10 16a1 1 0 0 1-2 0v-4a1 1 0 0 1 2 0zm0-11.67c0-.16.21-.33.5-.33h' +
        '3c.29 0 .5.17.5.33V6h-4zM16 16a1 1 0 0 1-2 0v-4a1 1 0 0 1 2 0z';
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="' + im_size + '"><path class="' + path_class + '" d="' + value + '"/></svg>';
}

/***************
** Attributes **
***************/
// TODO: AttributeForm anpassen / Wie bei Skills entsprechend einbauen.
function showAttributeForm(event) {
    var req_item = this;
    $.post('aj_get_attribute', {'attribute_id': req_item.id}, function(d_in){
        var row = $('tr#' + d_in.id);
        row.off('click');
        row.children('td.title').html('<input type="text" class="title" att_id="' + d_in.id + '" value="' + d_in.title + '" />');
        row.children('td.description').html('<input type="text" class="description" att_id="' + d_in.id + '" value="' + d_in.description + '" />');
        row.children('td.short').html('<input type="text" class="short" att_id="' + d_in.id + '" value="' + d_in.short + '" />');
        row.children('td.order').html('<input type="number" class="order" att_id="' + d_in.id + '" value="' + d_in.order + '" />');
        row.children('td.standard').html('<input type="checkbox" class="standard" att_id="' + d_in.id + '"' + (d_in.standard?' checked':'') + '/>');
        row.children('td.buttons').html(getButton("checkmark", "check", "medium") + getButton("trash", "trash", "medium"));

        var submit = $('tr#' + d_in.id + ' path.check');
        submit.attr('att_id', d_in.id);
        submit.on('click', submitAttributeForm);

        var del = $('tr#' + d_in.id + ' path.trash');
        del.attr('att_id', d_in.id);
        del.on('click', clickDeleteAttribute);
    });
}

function submitAttributeForm(event) {
    var id = event.target.getAttribute("att_id");
    d_out = {'att_id': id,
            'title': $('input.title[att_id="' + id + '"]').val(),
            'description': $('input.description[att_id="' + id + '"]').val(),
            'short': $('input.short[att_id="' + id + '"]').val(),
            'order': $('input.order[att_id="' + id + '"]').val(),
            'standard': ($('input.standard[att_id="' + id + '"]').is(':checked')? true: false)};
    $.post('aj_set_attribute', d_out, function(d_in){
        if(id=='new_attribute') {
            $('tr#new_attribute').attr('id', d_in.id);
        }
        var row = $('tr#' + d_in.id);
        row.children('td.title').text(d_in.title);
        row.children('td.description').text(d_in.description);
        row.children('td.short').text(d_in.short);
        row.children('td.order').text(d_in.order);
        row.children('td.standard').html(d_in.standard?'&check;':'x')
        row.children('td.buttons').html('');
        row.on('click', showAttributeForm);
    })
}

function clickDeleteAttribute(event) {
    var d_out = {'att_id': event.target.getAttribute("att_id")};
    $.post('aj_delete_attribute', d_out, function(d_in){
        if(d_in.deleted){
            $('tr#' + d_in.id).remove()
        }
    });
    event.preventDefault();
}

function clickNewAttribute(event){
    var new_tr = '<tr id="new_attribute" class="editable attribute">'
        + '<td class="title"><input type="text" class="title" att_id="new_attribute" value="" /></td>'
        + '<td class="description"><input type="text" class="description" att_id="new_attribute" value="" /></td>'
        + '<td class="short"><input type="text" class="short" att_id="new_attribute" value="" /></td>'
        + '<td class="order"><input type="number" class="order" att_id="new_attribute" value="" /></td>'
        + '<td class="standard"><input type="checkbox" class="standard" head_id="new_header" /></td>'
        + '<td class="buttons"><a href="javascript:void(0)" class="submit" att_id="new_attribute">(&check;)</a></td>'
        + '</tr>';
    if(!$('tr#new_attribute').length){
        $('table#attributes').append(new_tr);
        $('a.submit[att_id="new_attribute"]').on('click', submitAttributeForm);
    }
}


/****************
**             **
** Head-Values **
**             **
****************/
function showHeadForm(event) {
    var req_item = this;
    $.post('aj_get_head', {'head_id': req_item.id}, function(data){
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
            .html(getButton("checkmark", "check", "medium") + getButton("trash", "trash", "medium"));

        var submit = $('tr#' + data.id + ' path.check');
        submit.attr('head_id', data.id);
        submit.on('click', submitHeadForm);

        var del = $('tr#' + data.id + ' path.trash');
        del.attr('head_id', data.id);
        del.on('click', clickDeleteHead);
    });
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

function clickDeleteHead(event) {
    var d_out = {'head_id': event.target.getAttribute("head_id")};
    $.post('aj_delete_head', d_out, function(d_in){
        if(d_in.deleted){
            $('tr#' + d_in.id).remove()
        }
    });
    event.preventDefault();
}

function clickNewHead(event){
    var new_tr = '<tr id="new_header" class="editable head_value">'
        + '<td class="title"><input type="text" class="title" head_id="new_header" value="" /></td>'
        + '<td class="description"><input type="text" class="description" head_id="new_header" value="" /></td>'
        + '<td class="order"><input type="number" class="order" head_id="new_header" value="" /></td>'
        + '<td class="standard"><input type="checkbox" class="standard" head_id="new_header" /></td>'
        + '<td class="buttons"><a href="javascript:void(0)" class="submit" head_id="new_header">(&check;)</a></td>'
        + '</tr>';
    if(!$('tr#new_header').length) {
        $('table#headers').append(new_tr);
        $('a.submit[head_id="new_header"]').on('click', submitHeadForm);
    }
}


/***********
**        **
** Skills **
**        **
***********/
function showSkillForm(event) {
    var req_item = this;
    $.post('aj_get_skill', {'skill_id': req_item.id}, function(d_in){
        row = makeSkillForm(d_in);
        row.off('click');
    });
}

function makeSkillForm(d_in) {
    var s_id = d_in.id;
    row = $('tr#' + d_in.id);
    $.post('aj_get_attribute_list', {}, function(d_attribute_list){
        row.children('td.attribute_1').html(createSelect("att_1", 'skill_id', d_in.id, d_attribute_list.attribute_list, d_in.attribute_1));
        row.children('td.attribute_2').html(createSelect("att_2", 'skill_id', d_in.id, d_attribute_list.attribute_list, d_in.attribute_2));
        row.children('td.attribute_3').html(createSelect("att_3", 'skill_id', d_in.id, d_attribute_list.attribute_list, d_in.attribute_3));
    });
    row.children('td.title').html('<input type="text" class="title" skill_id="' + d_in.id + '" value="' + (s_id=="new_skill"? "": d_in.title) + '" />');
    row.children('td.description').html('<input type="text" class="description" skill_id="' + d_in.id + '" value="' + (s_id=="new_skill"? "": d_in.description) + '" />');
    row.children('td.order').html('<input type="number" class="order" skill_id="' + d_in.id + '" value="' + (s_id=="new_skill"? "0": d_in.order) + '" />');
    row.children('td.standard').html('<input type="checkbox" class="standard" skill_id="' + d_in.id + '"' + (d_in.standard?' checked':'') + '/>');
    row.children('td.buttons').html(getButton("checkmark", "check", "medium") + getButton("trash", "trash", "medium"));

    var submit = $('tr#' + d_in.id + ' path.check');
    submit.attr('skill_id', d_in.id);
    submit.on('click', submitSkillForm);

    var del = $('tr#' + d_in.id + ' path.trash');
    del.attr('skill_id', d_in.id);
    del.on('click', clickDeleteSkill);

    $('tr#' + d_in.id + ' input.title').focus();

    return row;
}

function submitSkillForm(event) {
    var id = event.target.getAttribute("skill_id");
    d_out = {'skill_id': id,
            'title': $('input.title[skill_id="' + id + '"]').val(),
            'description': $('input.description[skill_id="' + id + '"]').val(),
            'attribute_1': $('select.att_1[skill_id="' + id + '"').val(),
            'attribute_2': $('select.att_2[skill_id="' + id + '"').val(),
            'attribute_3': $('select.att_3[skill_id="' + id + '"').val(),
            'order': $('input.order[skill_id="' + id + '"]').val(),
            'standard': ($('input.standard[skill_id="' + id + '"]').is(':checked')? true: false)};
    console.log(d_out);
    $.post('aj_set_skill', d_out, function(d_in){
        console.log(d_in);
        if(id=='new_skill') {
            $('tr#new_skill').attr('id', d_in.id);
        }
        var row = $('tr#' + d_in.id);
        row.children('td.title').text(d_in.title);
        row.children('td.description').text(d_in.description);
        row.children('td.attribute_1').text(d_in.attribute_1);
        row.children('td.attribute_2').text(d_in.attribute_2);
        row.children('td.attribute_3').text(d_in.attribute_3);
        row.children('td.order').text(d_in.order);
        row.children('td.standard').html(d_in.standard?'&check;':'x')
        row.children('td.buttons').html('');
        row.on('click', showSkillForm);
    })
}

function clickDeleteSkill(event) {
    var d_out = {'skill_id': event.target.getAttribute("skill_id")};
    $.post('aj_delete_skill', d_out, function(d_in){
        if(d_in.deleted){
            $('tr.skill#' + d_in.id).remove()
        }
    });
    event.preventDefault();
}

function clickNewSkill(event){
    var new_tr = '<tr id="new_skill" class="editable skill">'
        + '<td class="title"></td>'
        + '<td class="description"></td>'
        + '<td class="attribute_1"></td>'
        + '<td class="attribute_2"></td>'
        + '<td class="attribute_3"></td>'
        + '<td class="order"></td>'
        + '<td class="standard"></td>'
        + '<td class="buttons"></td>'
        + '</tr>'
    if(!$('tr#new_skill').length){
        $('table#skills').append(new_tr);
        makeSkillForm({id: "new_skill"});
    }
}


/**************
**           **
** Listeners **
**           **
**************/
$('a#new_attribute').on('click', clickNewAttribute);
$('tr.attribute').on('click', showAttributeForm);

$('a#new_head').on('click', clickNewHead);
$('tr.head_value').on('click', showHeadForm);

$('a#new_skill').on('click', clickNewSkill);
$('tr.skill').on('click', showSkillForm);

// TODO: SameSite-Probleme in der Java-Console zu sehen
