const yourCoursesTab = document.getElementById('yourCoursesTab');
const addCoursesTab = document.getElementById('addCoursesTab');
const yourClassesContent = document.getElementById('yourClassesContent');
const addClassesContent = document.getElementById('addClassesContent');
const signOutElement = document.querySelector('.signOut');

function signOut()
{
    window.location.href = "login.html"; //return to login html page
}

if (signOutElement)
{
    signOutElement.addEventListener('click', signOut); // return to login when clicked
}

function activateTab(tab)
{
    yourCoursesTab.classList.remove('active');// remove the 'active' class from both tabs
    addCoursesTab.classList.remove('active');

    tab.classList.add('active');

    // toggle the visibility of content based on the active tab
    if (tab === yourCoursesTab) {
        yourClassesContent.style.display = 'block';
        addClassesContent.style.display = 'none';
    } else if (tab === addCoursesTab) {
        addClassesContent.style.display = 'block';
        yourClassesContent.style.display = 'none';
    }
}

function populateAddCoursesTab() // populate AddCourses tab by fetching api data
{
    fetch('http://127.0.0.1:5000/courses/1') 
        .then(response => response.json())
        .then(data => {
            const table = document.querySelector('#addClassesContent .centered-table tbody');
            table.innerHTML = ''; //clear content for new content
            data.forEach(course => { //iterates over each course object and populate for each row
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${course.Course}</td>
                    <td>${course.Teacher}</td>
                    <td>${course.Time}</td>
                    <td>${course.EnrolledNum}</td>
                    <td>${course.Capacity}</td>
                    <td button class="addClass">Add class</td>
                    <td button class="deleteClass">Delete Class</td>
                `;
                table.appendChild(row);
            });
        });  
}

document.addEventListener('click', function (event) { // add classes and delete them to the your classes tab
    if (event.target.classList.contains('addClass')) {
        const clickedRow = event.target.closest('tr');
        const course = { //take all content from each row and parse it to the function
            Course: clickedRow.cells[0].textContent,
            Teacher: clickedRow.cells[1].textContent,
            Time: clickedRow.cells[2].textContent,
            EnrolledNum: clickedRow.cells[3].textContent,
            Capacity: clickedRow.cells[4].textContent
        };
        addCourseToYourClasses(course);  // callback to function and add courses
    }

    if (event.target.classList.contains('deleteClass')) //delete instead
    {
        const clickedRow = event.target.closest('tr');
        const courseName = clickedRow.cells[0].textContent;

        deleteCourseFromYourClasses(courseName); // call back to function loop and remove each content from row
        
    }
});

function addCourseToYourClasses(course)
{
    const table = document.querySelector('#yourClassesContent .centered-table tbody');
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td>${course.Course}</td>
        <td>${course.Teacher}</td>
        <td>${course.Time}</td>
        <td>${course.EnrolledNum}</td>
        <td>${course.Capacity}</td>
    `;
    table.appendChild(newRow); //add each item to the row
}

function deleteCourseFromYourClasses(courseName) 
{
    const table = document.querySelector('#yourClassesContent .centered-table tbody');
    const rows = table.getElementsByTagName('tr');
    
    for (let i = 0; i < rows.length; i++) { // for each row until the last item in the index
        if (rows[i].cells[0].textContent === courseName) {//check first left most cell of content in the row. if matched to course name
            rows[i].remove(); // delete it
            break;
        }
    }
}

yourCoursesTab.addEventListener('click', () => { //when clicked run these functions
    activateTab(yourCoursesTab);  
});

addCoursesTab.addEventListener('click', () => { //when clicked run these functions
    activateTab(addCoursesTab);
    populateAddCoursesTab(); 
    
});


