const mediaQueryList = window.matchMedia("(max-width: 1200px)")

const sidebar = document.querySelector(".base-sidebar")
const sidebarToggle = document.querySelector(".sidebar-toggle-container")

function toggleVisibility(e) {
    console.log("Toggling visibility!")

    const sidebar = document.querySelector(".base-sidebar")

    if (sidebar.hasAttribute("hidden")) {
        sidebar.removeAttribute("hidden")
        sidebar.setAttribute("visible", "")
    } else {
        sidebar.removeAttribute("visible")
        sidebar.setAttribute("hidden", "")
    }
}

function applyOrRemoveVisibilityToggle(e) {
    const sidebar = document.querySelector(".base-sidebar")
    const sidebarToggle = document.querySelector(".sidebar-toggle-container")

    if (e.matches) {
        if (!sidebar.hasAttribute("visible")) {
            sidebar.setAttribute("hidden", "")
        }

        sidebarToggle.addEventListener("click", toggleVisibility)
    } else {
        sidebar.removeAttribute("hidden")
        sidebarToggle.removeEventListener("click", toggleVisibility)
    }
}

if (mediaQueryList.matches) {
    applyOrRemoveVisibilityToggle(mediaQueryList)
}

mediaQueryList.addListener(applyOrRemoveVisibilityToggle)