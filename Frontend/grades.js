function GET(course_id) {
    var url = "http://127.0.0.1:5000/courseGrade/1";
    // var url = "http://127.0.0.1:5000/courseGrade/1" + course_id;
    // var url = "http://lodocus.pythonanywhere.com/courseGrade/" + course_id;
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", url, true);
    xhttp.onload= function() {
        const rep = JSON.parse(this.responseText);

        var i;
        for(i = 0; i < rep.length; i++) {
            document.getElementById("namedisplay").innerHTML = `Welcome ${rep[i].Teacher}!`
            document.getElementById("coursename").innerHTML = `${rep[i].Course}`
            document.getElementById("gradesinfo").innerHTML += `<tr><td>${rep[i].Student}</td><td><a style = "text-decoration: none;color:white;" href="#edit"> ${rep[i].Grade} </a></td></tr>`
        }
    };
    xhttp.send();
} 

function PUT(course_id, user_id) {
    const promise = new Promise((resolve, reject) => {
        const xhttp = new XMLHttpRequest();
        const url = `http://127.0.0.1:5000/grades/${1}`;
        xhttp.open("PUT", url, true);
        xhttp.responseType = 'json';
        xhttp.setRequestHeader("Content-Type", "application/json");
        // const body = {'Grade': grade};
        // const body = {'grade': eval(document.getElementById("editedgrade").value)};
        // document.getElementById("coursename").innerHTML = `${course_id}`
        const body = {
            'grade' : eval(document.getElementById("editedgrade").value),
            'user_id': 1
        };
        // const body = {
        //     'grade' : eval(document.getElementById("editedgrade").value),
        //     'user_id': user_id
        // };
        xhttp.send(JSON.stringify(body));
        xhttp.onload = function() {
            resolve(xhttp.response);
    }
    });
    return promise
}


// function NAME() {
//     var url = "http://127.0.0.1:5000/teacherCourses/2";
//     var xhttp = new XMLHttpRequest();
//     xhttp.open("GET", url, true);
//     xhttp.onload= function() {
//         const rep = JSON.parse(this.responseText);

//         var i;
//         for(i = 0; i < rep.length; i++) {
//             document.getElementById("namedisplay").innerHTML = `Welcome ${rep[i].Teacher}!`
//         }
//     };
//     xhttp.send();
// } 


// function PUT(user_id) {
//     var xhttp = new XMLHttpRequest();
//     var url = "http://127.0.0.1:5000/grades/${user_id}";
//     xhttp.open("GET", url);
//     xhttp.onload = function() {
//         if(xhttp.status != 404) {
//             const payload = {
//                 "Grade": 100
//             }
//             var xtp = new XMLHttpRequest();
//             xtp.open("PUT", url, true);
//             xtp.setRequestHeader("Content-Type", "application/json");
//             xtp.onload = function() {
//                 if(xtp.status != 404) {
//                     const rep = JSON.parse(this.responseText);
//                     // document.getElementById("editedgrade").innerHTML = course_id;
//                 }
//             }
//             xtp.send(JSON.stringify(payload));
//         }
//         else {
//             document.getElementById("editedgrade").innerHTML = "ERROR";
//             // console.error("Error updating grade");
//         }
//     };
//     xhttp.send();
// }

