// تأكيد عند حذف كورس
function confirmDelete(courseTitle) {
    return confirm("هل أنت متأكد أنك تريد حذف الكورس: " + courseTitle + "؟");
}

// البحث عن كورسات
function filterCourses() {
    let input = document.getElementById("searchInput").value.toLowerCase();
    let items = document.getElementsByClassName("course-item");

    for (let i = 0; i < items.length; i++) {
        let title = items[i].getElementsByTagName("h3")[0].innerText.toLowerCase();
        items[i].style.display = title.includes(input) ? "" : "none";
    }
}

// قائمة منسدلة (Responsive Navbar)
function toggleMenu() {
    document.getElementById("nav-links").classList.toggle("show");
}