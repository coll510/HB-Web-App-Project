
let button = document.querySelector('#save-button');

function saveNow(evt) {
    evt.preventDefault();
    console.log("hello");
    // alert("I am saved!");
    console.log(document.getElementById('class-results'));
    //make AJAX post request with class info
    //add saved class info to database
    //$.post("/savedclasses", {"name": c;ass name, "start_time": start time});
    
    //don't leave the page though
    // in .py it would be something like INSERT INTO user_classes (user_id, 
    // class_id, class_saved)
    // VALUES (:user_id, class_id, :True)
    //;
}

button.addEventListener('click', saveNow);

// const button2 = document.querySelector('#attended-button');

// function trackNow(evt) {
//     //add attended class info to database
//     //don't leave the page though
//     //;
// }

// button.addEventListener('click', trackNow);