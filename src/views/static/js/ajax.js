class Form {
    constructor(form) {
        this.formvalues = form;
    }

    setID(id) {
        this.id = id;
    }

    loadForm() {
        var self = this;
        $.post(this.formvalues.getter, {'aj_id': self.id}, function(d_in){
            self.showForm(d_in);
        });
    }

    showForm(d_in) {
        var div = $('#edit');
        div.empty();

        var title = document.createElement('div');
        title.innerHTML = d_in['title'];

        var a = this.formvalues.form;
        for (const key in this.formvalues.form) {
            if (this.formvalues.form.hasOwnProperty(key)) {
                const element = this.formvalues.form[key];
                switch (element.type) {
                    case "hidden":
                        div.append(this.fieldHidden(d_in[key], key, element))
                        break;
                
                    default:
                        div.append(title);
                        break;
                }
            }
        }
    }

    fieldHidden(value, key, element) {
        var field = document.createElement('div');
        field.innerHTML = value;
        return field;
    }

    hookup() {
        var self = this;
        $('.' + this.formvalues.class).on('click', function(){
            self.setID($(this).attr('aj_id'));
            self.loadForm();
        });
    }
}
