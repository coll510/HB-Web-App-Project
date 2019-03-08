
function saveClass(evt) {
    evt.preventDefault();
    const form = $(evt.target);
    let formInputs = {
        "class_name": form.data('eventName'),
        "start_time": form.data('eventStart'), 
        "end_time": form.data('eventEnd'), 
        "url": form.data('eventUrl') 
    };
        $.post('/saved-classes', formInputs, (message) => {
           $('#confirm-save-msg').html(message);  
           console.log(message)
        });

       

}

$('.show-class').on('submit', saveClass);