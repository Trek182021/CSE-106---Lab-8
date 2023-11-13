function GET(id) {
    var url = "http://127.0.0.1:5000/teacherCourses/2";
    // var url = "http://lodocus.pythonanywhere.com/teacherCourses/" + id;
    // var url = "http://127.0.0.1:5000/teacherCourses/" + id;
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", url, true);
    xhttp.onload= function() {
        const rep = JSON.parse(this.responseText);

        // document.getElementById("courseinfo").innerHTML += `<td>${rep.display}</td>`
        var i;
        for(i = 0; i < rep.length; i++) {
            document.getElementById("courseinfo").innerHTML += `<tr><td><a href="grades.html"> ${rep[i].Course} </a></td><td>${rep[i].Teacher}</td><td>${rep[i].Time}</td><td>${rep[i].EnrolledNum}/${rep[i].Capacity}</td></tr>`
            document.getElementById("namedisplay").innerHTML = `Welcome ${rep[i].Teacher}!`
        }

        // for(objs in rep){ console.log(objs);
        //     var th = document.createElement('th');
        //     document.getElementById("courseinfo").innerHTML += `<tr><td>${objs}</td><td>${rep[objs]}</td></tr>`
        //     // document.getElementById("courseinfo").innerHTML += `<td>${rep.Course}</td>`
        // }
    };
    xhttp.send();
} 

