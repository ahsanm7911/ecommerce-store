let sidebarContainer = document.getElementById('sidebarContainer')
let navbarContainer = document.getElementById('navbarContainer')

function toggleSidebar(){
    if(navbarContainer.classList.contains("d-none")){
        navbarContainer.classList.remove("d-none")
        sidebarContainer.classList.add("d-none")
    } else {
        navbarContainer.classList.add("d-none")
        sidebarContainer.classList.remove("d-none")
    }
}