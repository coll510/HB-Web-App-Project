
const button = document.querySelector('#save-button');

function saveNow(evt) {
    //add saved class info to database
    //don't leave the page though
    // in .py it would be something like INSERT INTO user_classes (user_id, 
    // class_id, class_saved)
    // VALUES (:user_id, class_id, :True)
    //;
}

button.addEventListener('click', saveNow);

const button = document.querySelector('#attended-button');

function trackNow(evt) {
    //add attended class info to database
    //don't leave the page though
    //;
}

button.addEventListener('click', trackNow);