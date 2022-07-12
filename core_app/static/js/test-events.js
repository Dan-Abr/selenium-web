// Find the 'Add New Action' button to add test functionalities (wait, click, etc)
// Source - https://medium.com/all-about-django/adding-forms-dynamically-to-a-django-formset-375f1090c2b0


function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}


function cloneMore(selector, prefix) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
        if ($(this).attr('name')){
            var name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        }
    });

    newElement.find('label').each(function() {
        var forValue = $(this).attr('for');
        if (forValue) {
          forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
          $(this).attr({'for': forValue});
        }
    });

    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    var conditionRow = $('.action-form:not(:last)');
    
    conditionRow.find('.btn.add-form-row')
    .removeClass('btn-success').addClass('btn-danger')
    .removeClass('add-form-row').addClass('remove-form-row')
    .html('<span class="glyphicon glyphicon-minus" aria-hidden="true">REMOVE</span>');


    newElement.find('.action-title').html('Action' + ' ' + total)
    return false;
}


function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1){
        btn.closest('.action-form').remove();
        var forms = $('.action-form');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex(this, prefix, i);
            });
            $(forms.get(i)).find('.action-title').html('Action' + ' ' + (i+1))
        }
    }
    return false;
}


$(document).on('click', '.add-form-row', function(e){
    console.log("what")
    e.preventDefault();
    cloneMore('.action-form:last', 'form');
    return false;
});


$(document).on('click', '.remove-form-row', function(e){
    e.preventDefault();
    deleteForm('form', $(this));
    return false;
});