const yourCoursesTab = document.getElementById('yourCoursesTab');
const addCoursesTab = document.getElementById('addCoursesTab');
const yourClassesContent = document.getElementById('yourClassesContent');
const addClassesContent = document.getElementById('addClassesContent');

// Function to handle tab activation
function activateTab(tab)
{
    // Remove the 'active' class from both tabs
    yourCoursesTab.classList.remove('active');
    addCoursesTab.classList.remove('active');

    // Add the 'active' class to the clicked tab
    tab.classList.add('active');

    // Toggle the visibility of content based on the active tab
    if (tab === yourCoursesTab) {
        yourClassesContent.style.display = 'block';
        addClassesContent.style.display = 'none';
    } else if (tab === addCoursesTab) {
        addClassesContent.style.display = 'block';
        yourClassesContent.style.display = 'none';
    }
}

// Add click event listeners to the tabs
yourCoursesTab.addEventListener('click', () => {
    activateTab(yourCoursesTab);
});

addCoursesTab.addEventListener('click', () => {
    activateTab(addCoursesTab);
});