// Extension to - https://medium.com/all-about-django/adding-forms-dynamically-to-a-django-formset-375f1090c2b0

// ---------------------------------------------------------------------------------
// Clone & Delete Forms
// ---------------------------------------------------------------------------------
var maxForms = 7
var minForms = 1
var editPage = 'edit'
var createPage = 'create'
var firstActionForm = 'form-0'
var totalFormsOnLoad = parseInt($('#id_form-TOTAL_FORMS').val());


function updateFormIndex(form, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(form).attr("for")) $(form).attr("for", $(form).attr("for").replace(id_regex, replacement));
    if (form.id) form.id = form.id.replace(id_regex, replacement);
    if (form.name) form.name = form.name.replace(id_regex, replacement);
}


function cloneForm(selector, prefix) {
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();

    // Copy the last form as it is with a MINUS button so the newly
    // created from will already have a MINUS button.
    var newForm = $(selector).clone(true);

    if(total < maxForms){
        // If there is only one form, create a MINUS button (total == 1) after cloning it
        // since it doesn't have this button.
        if(total == minForms){
            if(window.location.href.indexOf(createPage) > 0){
                form_btn_minus = $("<button>", {"type": "button", "class": "btn btn-danger remove-form-row"}).text("-");
                // Create the MINUS button after the PLUS button
                newForm.find('.card-body').find('.add-form-row').before(form_btn_minus);
            } else if(window.location.href.indexOf(editPage) > 0){
                // In the edit page buttons can't be deleted and must be marked first.
                // Thus, the color of the buttons should be neutral unless they are
                // being clicked.
                form_btn_minus = $("<button>", {"type": "button", "class": "btn btn-secondary remove-form-row"}).text("-");
                // Create the MINUS button after the PLUS button
                newForm.find('.card-body').find('.add-form-row').before(form_btn_minus);
            }
        }

        // Prevent duplicate MINUS buttons after duplications in previous forms.
        var form_btn_minus = $(selector).find('.card-body').find('.remove-form-row')
        if(form_btn_minus != undefined){
            $(selector).find('.card-body').find('.remove-form-row').remove();
        }

        // Update the new form's inputs (indices)
        newForm.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
            if ($(this).attr('name')){
                var name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
                var id = 'id_' + name;
                $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
            }
        });

        // Update the new form's labels (indices)
        newForm.find('label').each(function() {
            var forValue = $(this).attr('for');
            if (forValue) {
                forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
                $(this).attr({'for': forValue});
            }
        });

        // Update the new form's id
        var formId = newForm.attr('id');
        formId = formId.replace('-' + (total-1), '-' + total);
        newForm.attr("id", formId)

        total++;
        $('#id_' + prefix + '-TOTAL_FORMS').val(total);
        $(selector).after(newForm);
        var allFormsExceptLast = $('.action-form:not(:last)');

        // Replace the PLUS button with a MINUS button
        if(window.location.href.indexOf(createPage) > 0){
            allFormsExceptLast.find('.btn.add-form-row')
            .removeClass('btn-success').addClass('btn-danger')
            .removeClass('add-form-row').addClass('remove-form-row')
            .html('<span class="glyphicon glyphicon-minus" aria-hidden="true">-</span>');
        } else if(window.location.href.indexOf(editPage) > 0){
            allFormsExceptLast.find('.btn.add-form-row')
            .removeClass('btn-success').addClass('btn-secondary')
            .removeClass('add-form-row').addClass('remove-form-row')
            .html('<span class="glyphicon glyphicon-minus" aria-hidden="true">-</span>');
        }

        // Update the title with the right number
        newForm.find('.action-title').html('Action' + ' ' + total);
    }
    if(total == maxForms){
        // Remove the PLUS button on the last form
        newForm.find('.btn.add-form-row').remove();

    }
    return false;
}


function deleteFormOnCreation(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());

    // Retain one form
    if (total > minForms){
        btn.closest('.action-form').remove();

        // Add the PLUS button to the newest last form 
        var last_form = $('.action-form:last').find('.card-body');
        var form_btn_plus = last_form.find('.add-form-row');
        // If it already has a PLUS button, don't add another one.
        // Check for length since it also returns the previous object and hence not undefined.
        if(form_btn_plus.length == 0){
            form_btn_plus = $("<button>", {"type": "button", "class": "btn btn-success add-form-row"}).text("+");
            last_form.append(form_btn_plus);
        }

        // Update the form components' indices
        var forms = $('.action-form');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).find(':input', 'input[type=hidden]').each(function() {
                updateFormIndex(this, prefix, i);
            });
            // Update the form's id
            updateFormIndex(forms.get(i), prefix, i);
            // Update the title in the form
            $(forms.get(i)).find('.action-title').html('Action' + ' ' + (i+1));
        }
    }
    // After the deletion of the form above (total == 2), if only one form left
    // it shouldn't have a MINUS button.
    if(total == 2){
        var form = $('.action-form:first');
        form.find('.card-body').find('.remove-form-row').remove();
    }
    return false;
}


function deleteFormOnEdit(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    var actionForm = btn.closest('.action-form');

    // Do not allow the deletion of the first form
    if (total > minForms && actionForm.attr('id') != firstActionForm){
        var actionFormDeletionCheck = actionForm.find('input[type="checkbox"]')
        var checkedForDeletion = actionFormDeletionCheck.prop('checked')
        
        // If the element is unchecked for deletion, check it.
        if(!checkedForDeletion){
            // Check the 'Delete' field to delete the form
            actionFormDeletionCheck.prop('checked', true)

            // Feedback of red-colored button for the form to be deleted
            actionForm.find('.btn.btn-secondary')
            .removeClass('btn-secondary').addClass('btn-danger')
        }
        // Forms which previously added, must remove them with POST
        else{
            // Remove the check from the 'Delete' field
            actionFormDeletionCheck.prop('checked', false)

            // Feedback of gray-colored button as it won't be deleted
            actionForm.find('.btn.btn-danger')
            .removeClass('btn-danger').addClass('btn-secondary')
        }

    }
    // Form added during this session - allow to delete on-spot.
    // (totalFormsOnLoad-1) since the count starts on 0
    if(parseInt(actionForm.attr('id').match(/\d+/)) > (totalFormsOnLoad-1)){
        deleteFormOnCreation('form', btn)
    }
    return false;
}



// ---------------------------------------------------------------------------------
// Update Forms' Fields (wait, click)
// ---------------------------------------------------------------------------------
var waitTimeField = 'wait_time_in_sec';
var cssSelectorField = 'css_selector_click'
var firstActionFormId = '#form-0'


// On the edit page, iterate all the existing action-forms and hide irrelevant fields.
$(document).ready(function(){
    if(window.location.href.indexOf(editPage) > 0){
        // Hide actionTypes based on the user's choice for the form
        $(document).find('.action-form').each(function() {
            var actionType = $(this).find('select').val()
            hideShowFormFields(this, actionType)
        });
        // Remove deletion option for the first form
        var actionForm = $(document).find(firstActionFormId);
        if (actionForm != undefined){
            actionForm.find('label:last').remove()
            actionForm.find('input[type="checkbox"]').remove()
        }
    }
});


// Helper function to hide/show relevant fields based on the user's choice.
function hideShowFormFields(form, selectedValue){
    form = $(form)
    switch (selectedValue) {
        case "1":
            // If the chosen action is 'Wait', hide unrelated fields
            form.closest('.action-form').find('input[id$='+waitTimeField+'], label[for$='+waitTimeField+']').each(function() {
                $(this).show();
            });
            form.closest('.action-form').find('input[id$='+cssSelectorField+'], label[for$='+cssSelectorField+']').each(function() {
                $(this).val('')
                $(this).hide();
            });
            break;
        case "2":
            // If the chosen action is 'Click', hide unrelated fields
            form.closest('.action-form').find('input[id$='+cssSelectorField+'], label[for$='+cssSelectorField+']').each(function() {
                $(this).show();
            });
            form.closest('.action-form').find('input[id$='+waitTimeField+'], label[for$='+waitTimeField+']').each(function() {
                $(this).val('')
                $(this).hide();
            });
            break;
    }
}


// On page load, set the first form with a 'Wait' action and hide any other field.
// This is for the page where the user creates new tests.
$(document).ready(function(){
    if(window.location.href.indexOf(createPage) > 0){
        $(document).find(firstActionFormId).find('input[id$='+cssSelectorField+']').each(function() {
            // If the CSS selector field is empty hide it (not in edit mode)
            if(!$(this).val()){
                $(document).find(firstActionFormId).find('label[for$='+cssSelectorField+']').hide();
                $(this).val('')
                $(this).hide();
            }
        });
    }
});



// ---------------------------------------------------------------------------------
// Triggers
// ---------------------------------------------------------------------------------
// When the user clicks on new form, create a clone
$(document).on('click', '.add-form-row', function(e){
    e.preventDefault();
    cloneForm('.action-form:last', 'form');
    return false;
});


// When the user clicks on remove form, delete/mark it
$(document).on('click', '.remove-form-row', function(e){
    e.preventDefault();
    if(window.location.href.indexOf(createPage) > 0){
        deleteFormOnCreation('form', $(this));
    }
    else if(window.location.href.indexOf(editPage) > 0){
        deleteFormOnEdit('form', $(this));
    }
    return false;
});


// When the user changes the chooses action, update the form
// with the relevant fields for that action.
$('select').on('change', function(e) {
    hideShowFormFields(this, this.value);
    return false;
});