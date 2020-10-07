class Form {
    self = this;

    constructor(form) {
        this.formname = form['name'];
        this.div = form['div'];
        this.form = form['form'];
        this.class = form['class'];
    }

    setID(id) {
        this.id = id;
    }

    showForm() {
        $('#edit').html(this.formname+"<br />"+this.id);
        console.log(this.formname);
        console.log(this.form);
    }

    test() {
        console.log(this.class);
    }

    hookup() {
        var self = this;
        $('.' + this.class).on('click', function(){
            self.setID($(this).attr('ajax_id'));
            self.showForm();
        });
    }
}

/*
var form_id = "";
var form_form = "";
var form;

function showForm(){
    form_id = this.getAttribute('ajax_id');
    form_form = this.getAttribute('ajax_form');

    aj_function = 'aj_get_' + form_form;

    $('[ajax_id="' + form_id + '"]').off('click');

    $.post(aj_function, {'aj_id': form_id}, function(d_in){
        form = makeForm(d_in);
    });
}

function makeForm(d_in) {
    console.log(d_in);
}

function submitForm() {
}

function remove() {
}

function showFormForAjax() {
    form = new Form(forms[$(this).attr('ajax_form')]);
    form.setID($(this).attr('ajax_id'));
    form.showForm();
}
*/