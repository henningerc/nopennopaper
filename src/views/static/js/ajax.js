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

        this.values = d_in;

        var title = document.createElement('div');
        title.innerHTML = d_in['title'];

        var a = this.formvalues.form;
        for (const key in this.formvalues.form) {
            if (this.formvalues.form.hasOwnProperty(key)) {
                const element = this.formvalues.form[key];
                switch (element.type) {
                    case "hidden":
                        div.append(this.fieldHidden(d_in[key], key))
                        break;
                    case "text":
                        div.append(this.fieldText(d_in[key]));
                        break;
                    case "select_input":
                        div.append(this.fieldSelectInput(d_in[key], key, element));
                        break;
                    default:
                        break;
                }
            }
        }
    }

    fieldHidden(value, key) {
        var field = document.createElement('input');
        field.setAttribute('type', 'hidden');
        field.setAttribute('name', key);
        field.setAttribute('value', value)
        return field;
    }

    fieldText(value) {
        var field = document.createElement('div');
        field.innerHTML = value;
        return field;
    }

    fieldSelectInput(value, key, element) {
        var field = document.createElement('div');
        field.append(this.fieldSelect(value, key, element));
        return field;
    }

    fieldSelect(value, key, element) {
        var field = document.createElement('select');
        field.setAttribute('name', key);
                
        var filter = {};
        filter[element.filter.key] = this.values[element.filter.value_field];
        
        var option;
        option = document.createElement('option');
        option.setAttribute('value', 'null');
        option.innerHTML = '';
        field.append(option);
        $.post(element.list_source, filter, function(d_in){
            for(var v in d_in) {
                option = document.createElement('option');
                option.setAttribute('value', d_in[v].id);
                option.innerHTML = d_in[v].text;
                if(d_in[v].id==value) option.setAttribute('selected', 'true');
                field.append(option);
            }
        });
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
