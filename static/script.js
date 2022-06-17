// Navbar toggle
const NAVBAR = document.querySelector('nav')

document.querySelector('.toggle-menu').addEventListener('click', () => {
    NAVBAR.classList.add('active')
})

document.querySelector('.navbar__close').addEventListener('click', () => {
    NAVBAR.classList.remove('active')
})

// Dropdown menu
const SELECTED = document.querySelector('.select__selected')
const OPTIONS_CONTAINER = document.querySelector('.select__options')
const OPTIONS = document.querySelectorAll('.select__option')

// Toggle visibility of dropdown menu
SELECTED.addEventListener('click', () => {
    OPTIONS_CONTAINER.classList.toggle('active')
})

OPTIONS.forEach(option => {
    option.addEventListener('click', () => {
        // Change selected filter value
        SELECTED.innerHTML = option.innerHTML

        // Remove active style effect from previous option
        OPTIONS.forEach(option => {
            option.classList.remove('active')
        })
        
        // Add active style effect to new option
        option.classList.add('active')

        // Close dropdown menu
        OPTIONS_CONTAINER.classList.remove('active')
    })
})

// TODO: Change display to none for every unselected item
