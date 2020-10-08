function activateGridElement(index) {
    $.post('/activate/' + index);
}

$('#config-btn').click(function () {
    $('#config-modal').show();
});

$('#config-modal-close').click(function () {
    $('#config-modal').hide();
});

$('#action-select').change(function() {
    var actionSelector = '#' + $('#action-select').val();
    $('#config-fields').show();
    $('#config-fields').children().hide();
    $(actionSelector).show();
    $('#config-modal-save').show();
});

$('#config-modal-save').click(function () {
    var selectedAction = $('#action-select').val();

    // don't do anything if the action wasn't picked
    if (selectedAction == "")
        return;

    // make selectedElement an integer
    var selectedElement = parseInt($('#element-select').val());

    // setup fieldData information from config "form"
    var configFieldData = [];
    var configFields   = $('#config-fields')
        .children('#' + selectedAction)
        .children('input')
        .toArray();
    // add the field data to the array
    for (var i = 0; i < configFields.length; i++) {
        var element = configFields[i];
        configFieldData[configFieldData.length] = {'field': element.name, 'value': element.value};
    }

    // remove action prefix to allow us to turn the action into an int identifier
    selectedAction = parseInt(selectedAction.replace('action', ''));
 
    // setup the payload
    var fieldData = { 
        'element': selectedElement, 
        'action': selectedAction, 
        'fields': configFieldData
    }

    // make an AJAX call to the /config route to let flask handle the update
    $.ajax({
        url: '/config', 
        type: 'POST',
        data: JSON.stringify(fieldData),
        processData: false,
        contentType: 'application/json',
        success: function() {
            $('#config-modal').hide();  // close the modal when the AJAX works
        }
    });
});
