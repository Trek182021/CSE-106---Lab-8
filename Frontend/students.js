const yourCoursesTab = document.getElementById('yourCoursesTab');
const addCoursesTab = document.getElementById('addCoursesTab');
const yourClassesContent = document.getElementById('yourClassesContent');
const addClassesContent = document.getElementById('addClassesContent');
const userGreeting = document.getElementById('userGreeting');
const signOutElement = document.querySelector('.signOut');

userGreeting.textContent = `hello ${studentId}!`; //update user hello greetings

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

function populateYourCoursesTab() {
    fetch('Backend/api/studentCourses/<student_id>') 
        .then(response => response.json())
        .then(data => {
            const table = document.querySelector('#yourClassesContent .centered-table tbody');
            table.innerHTML = '';

            data.forEach(course => { //iterates over each course object and populate for each row
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${course.Course}</td>
                    <td>${course.Teacher}</td>
                    <td>${course.Time}</td>
                    <td>${course.EnrolledNum}</td>
                `;
                table.appendChild(row);
            });
        });
}


function populateAddCoursesTab() // populate AddCourses tab by fetching api data
{
    fetch('Backend/api/courses/<int:student_id>')
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
                    <td button class="addClass">Add class</td>
                    <td button class="deleteClass">Delete Class</td>
                `;
                table.appendChild(row);
            });
        });  
}

function signOut()
{
    window.location.href = "login.html"; //return to login html page
}


if (signOutElement)
{
    signOutElement.addEventListener('click', signOut); // return to login when clicked
}

yourCoursesTab.addEventListener('click', () => { //when clicked run these functions
    activateTab(yourCoursesTab);
    populateYourCoursesTab()
});

addCoursesTab.addEventListener('click', () => { //when clicked run these functions
    activateTab(addCoursesTab);
    populateAddCoursesTab(); 
});


