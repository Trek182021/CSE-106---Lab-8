function GET() {
    var url = "http://127.0.0.1:5000/teacherCourses/" + teacher_id;
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", url, true);
    xhttp.onload= function() {
        const rep = JSON.parse(this.responseText);
        for(objs in rep){ console.log(objs);
            var th = document.createElement('th');
            document.getElementById("courseinfo").innerHTML += `<tr><td>${objs}</td><td>${rep[objs]}</td></tr>`
        }
    };
    xhttp.send();
} 

function PUT(grade) {
    var xhttp = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/grades/" + course_id;
    xhttp.open("GET", url);
    xhttp.onload = function() {
        if(xhttp.status != 404) {
            // const payload = {
            //     grade: eval(document.getElementById("update_grade").value)
            // }
            var xtp = new XMLHttpRequest();
            xtp.open("PUT", url, true);
            xtp.setRequestHeader("Content-Type", "application/json");
            xtp.onload = function() {
                if(xtp.status != 404) {
                    const rep = JSON.parse(this.responseText);
                    document.getElementById("updatedgrade").innerHTML = course_id;
                }
            }
            xtp.send(JSON.stringify(payload));
        }
        else {
            document.getElementById("updatedgrade").innerHTML = "ERROR"
        }
    };
    xhttp.send();
}




// document.addEventListener('DOMContentLoaded', function () {
//     // Function to send a GET request to retrieve teacher's course info
//     function getTeacherCourseInfo(teacherId) {
//         fetch(`/teacherCourses/${teacherId}`, {
//             method: 'GET',
//             headers: {
//                 'Accept': 'application/json',
//             }
//         })
//         .then(response => response.json())
//         .then(data => {
//             // Handle the response data and display it on the webpage
//             displayTeacherCourseInfo(data);
//         })
//         .catch(error => {
//             console.error('Error:', error);
//         });
//     }

//     // Function to display teacher's course info on the webpage
//     function displayTeacherCourseInfo(courses) {
//         const outputDiv = document.getElementById('output');
//         outputDiv.innerHTML = '<h2>Teacher Course Information</h2>';
        
//         if (courses.length === 0) {
//             outputDiv.innerHTML += '<p>No courses found for this teacher.</p>';
//         } else {
//             const courseList = document.createElement('ul');

//             courses.forEach(course => {
//                 const courseItem = document.createElement('li');
//                 courseItem.textContent = `Course: ${course.Course}, Teacher: ${course.Teacher}, Time: ${course.Time}, EnrolledNum: ${course.EnrolledNum}, Capacity: ${course.Capacity}`;
//                 courseList.appendChild(courseItem);
//             });

//             outputDiv.appendChild(courseList);
//         }
//     }

//     // Call the getTeacherCourseInfo function with the teacher's ID (replace with the actual teacher ID)
//     const teacherId = 123; // Replace with the actual teacher's ID
//     getTeacherCourseInfo(teacherId);
// });
