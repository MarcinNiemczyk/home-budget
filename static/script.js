// Navbar toggle
const NAVBAR = document.querySelector('nav')

document.querySelector('.toggle-menu').addEventListener('click', () => {
    NAVBAR.classList.add('active')
})

document.querySelector('.navbar__close').addEventListener('click', () => {
    NAVBAR.classList.remove('active')
})

// Handle dropdown menu display
function dropdownMenu(NAME) {
    const SELECTED = document.querySelector('.' + NAME + '__selected')
    const OPTIONS_CONTAINER = document.querySelector('.' + NAME)
    const OPTIONS = document.querySelectorAll('.' + NAME+ '__option label')

    // Toggle visibility of dropdown menu
    SELECTED.addEventListener('click', () => {
        OPTIONS_CONTAINER.classList.toggle('active')
    })

    // Handle options interaction
    OPTIONS.forEach(option => {
        option.addEventListener('click', () => {
            // Change selected option value
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
}

// Track current page route
let currentPage = window.location.pathname

// Apply right functionality
if (currentPage == '/transactions') {
    dropdownMenu('filter')
    dropdownMenu('months')
    dropdownMenu('years')
} else if (currentPage == '/transactions/add') {
    dropdownMenu('category')

    // Change available categories depending on selected transaction type
    const TRANSACTION_TYPE = document.querySelector('.form__radio-container')
    TRANSACTION_TYPE.addEventListener('change', () => {
        // Toggle visibility of each option
        document.querySelectorAll('.category__option').forEach(option => {
            // Income categories are hidden by default
            option.classList.toggle('disabled')
        })
        // Reset selected category
        document.querySelector('.category__selected').innerHTML = 'Select Category'
        document.querySelectorAll('input[name="category__radio"]').forEach(radioButton => {
            radioButton.checked = false
        })
    })
}
