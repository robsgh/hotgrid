function clearModalValues() {
    $('#action-select').val('');
    $('#element-select').val('1');
    $('#config-fields').find('input').val('');
}

// send activate command to Flask
function activateGridElement(index) {
    $.ajax({
        url: '/api/hotgrid', 
        type: 'POST',
        data: JSON.stringify({'element': index - 1, 'active': true}),
        processData: false,
        contentType: 'application/json',
        success: function(data) {
            // get response data
            var element = data['element'] + 1;
            var active = data['active'];
            // if the server asserts that the element is active, activate it
            if (active == true) 
                $('#grid-' + element).addClass('is-dark');
            else
                $('#grid-' + element).removeClass('is-dark');
        }
    });
}

function changeGridElementIcon(index, icon_image_url) {
    $.ajax({
        url: '/api/hotgrid', 
        type: 'POST',
        data: JSON.stringify({'element': index-1, 'icon_image': icon_image_url}), 
        processData: false, 
        contentType: 'application/json', 
        success: function(data) {
            // get response data
            var element = data['element'] + 1;
            var icon_image = data['icon_image'];

            $('#grid-' + element).find('img').attr('src', icon_image);
        }
});
}

$('#config-btn').click(function () {
    $('#config-modal').show();
});
$('#config-modal-close').click(function () {
    $('#config-modal').hide();
});

// change options shown to user when the action select is modified
// this is fine to do on change since modal is reset when saved
$('#action-select').change(function() {
    var actionSelector = '#' + $('#action-select').val();
    $('#config-fields').show();
    $('#config-fields').children().hide();
    $(actionSelector).show();
    $('#config-modal-save').show();
});

$('#element-icon').change(function() {
    var filename = $('#element-icon').prop('files')[0].name;
    $('#element-icon-label').html(filename);
});

$('#config-modal-save').click(function () {
    var selectedAction = $('#action-select').val();
    var iconUpload = $('#element-icon');

    // make selectedElement an integer
    // make it into 0-based index for server communication
    var selectedElement = parseInt($('#element-select').val()) - 1;

    if (iconUpload.prop('files')) {
        if (iconUpload.prop('files').length > 0) {
            // create a pseudo-form with the file data
            var formData = new FormData();
            formData.append('file', iconUpload.prop('files')[0]);

            // send the request to upload an icon
            $.ajax({
                url: '/api/hotgrid/icon',
                type: 'POST',
                data: formData,
                contentType: false,
                processData: false,
                cache: false,
                success: function(data) {
                    var icon_name = data['icon_image'];

                    $('#config-modal').hide();
                    changeGridElementIcon(selectedElement + 1, icon_name);
                }
            });
        }
    }

    // don't config if the action wasn't picked
    if (selectedAction == "")
        return;

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
    // again, make it 0-based for server communication
    selectedAction = parseInt(selectedAction.replace('action', '')) - 1;
 
    // setup the payload
    var fieldData = { 
        'element': selectedElement, 
        'action': selectedAction, 
        'fields': configFieldData
    }

    // make an AJAX call to the /config route to let flask handle the update
    $.ajax({
        url: '/api/config', 
        type: 'POST',
        data: JSON.stringify(fieldData),
        processData: false,
        contentType: 'application/json',
        success: function(data) {
            clearModalValues();

            // get response data
            var element = data['element'] + 1;
            var enabled = data['enabled'];
            // if the server asserts that the element is enabled, enable it
            if (enabled == true) 
                $('#grid-' + element).click(function() {
                    activateGridElement(element);
                });

            $('#config-modal').hide();  // close the modal when the AJAX works
        }
    });
});

$('document').ready(clearModalValues());