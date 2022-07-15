// Source - https://medium.com/all-about-django/adding-forms-dynamically-to-a-django-formset-375f1090c2b0


function updateFormIndex(form, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(form).attr("for")) $(form).attr("for", $(form).attr("for").replace(id_regex, replacement));
    if (form.id) form.id = form.id.replace(id_regex, replacement);
    if (form.name) form.name = form.name.replace(id_regex, replacement);
}


function cloneMore(selector, prefix) {
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();

    // Copy the last form as it is with a MINUS button so the newly
    // created from will already have a MINUS button.
    var newForm = $(selector).clone(true);

    // Max of 7 forms
    if(total < 7){

        // If there is only one form, create a MINUS button (total == 1) after cloning it
        // since it doesn't have this button.
        if(total == 1){
            form_btn_minus = $("<button>", {"type": "button", "class": "btn btn-danger remove-form-row"}).text("-")
            // Create the MINUS button after the PLUS button
            newForm.find('.card-body').find('.add-form-row').before(form_btn_minus)
        }

        // Prevent duplicate MINUS buttons after duplications.
        var form_btn_minus = $(selector).find('.card-body').find('.remove-form-row')
        if(form_btn_minus != undefined){
            $(selector).find('.card-body').find('.remove-form-row').remove();
        }

        // Update the form component's indices
        newForm.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
            if ($(this).attr('name')){
                var name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
                var id = 'id_' + name;
                $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
            }
        });

        // Update the form labels' indices
        newForm.find('label').each(function() {
            var forValue = $(this).attr('for');
            if (forValue) {
            forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
            $(this).attr({'for': forValue});
            }
        });

        total++;
        $('#id_' + prefix + '-TOTAL_FORMS').val(total);
        $(selector).after(newForm);
        var allFormsExceptLast = $('.action-form:not(:last)');

        // Replace the PLUS button with a MINUS button
        allFormsExceptLast.find('.btn.add-form-row')
        .removeClass('btn-success').addClass('btn-danger')
        .removeClass('add-form-row').addClass('remove-form-row')
        .html('<span class="glyphicon glyphicon-minus" aria-hidden="true">-</span>');

        // Update the title with the right number
        newForm.find('.action-title').html('Action' + ' ' + total)
    }
    if(total == 7){
        // Remove the PLUS button on the 7th form
        newForm.find('.btn.add-form-row').remove()

    }
    return false;
}


function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());

    // Retain one form
    if (total > 1){
        // Delete the last form
        btn.closest('.action-form').remove();

        // Add the PLUS button to the newest last form 
        var last_form = $('.action-form:last').find('.card-body')
        var form_btn_plus = last_form.find('.add-form-row')
        // If it already has a PLUS button, don't add another one.
        // Check for length since it also returns the previous object and hence not undefined.
        if(form_btn_plus.length == 0){
            form_btn_plus = $("<button>", {"type": "button", "class": "btn btn-success add-form-row"}).text("+")
            last_form.append(form_btn_plus);
        }

        // Update the form component's indices
        var forms = $('.action-form');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateFormIndex(this, prefix, i);
            });
            $(forms.get(i)).find('.action-title').html('Action' + ' ' + (i+1))
        }
    }
    // After the deletion of the form above (total == 2), if only one form left
    // it shouldn't have a MINUS button.
    if(total == 2){
        var form = $('.action-form:first')
        form.find('.card-body').find('.remove-form-row').remove();
    }
    return false;
}


$(document).on('click', '.add-form-row', function(e){
    e.preventDefault();
    cloneMore('.action-form:last', 'form');
    return false;
});


$(document).on('click', '.remove-form-row', function(e){
    e.preventDefault();
    deleteForm('form', $(this));
    return false;
});