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
    const OPTIONS = document.querySelectorAll('.' + NAME+ '__option .radio')

    // Toggle visibility of dropdown menu
    SELECTED.addEventListener('click', () => {
        OPTIONS_CONTAINER.classList.toggle('active')
    })

    // Handle options interaction
    OPTIONS.forEach(option => {
        option.addEventListener('click', () => {
            // Change selected option value
            let label = document.querySelector('label[for="' + option.id + '"]')
            SELECTED.innerHTML = label.innerHTML

            // Remove active style effect from previous option
            OPTIONS.forEach(option => {
                let label = document.querySelector('label[for="' + option.id + '"]')
                label.classList.remove('active')
                option.checked = false
            })
            
            // Add active style effect to new option
            label.classList.add('active')
            option.checked = true

            // Close dropdown menu
            OPTIONS_CONTAINER.classList.remove('active')
        })
    })
}


function removeTransaction(transactionId) {
    fetch('/remove-transaction', {
        method: 'POST',
        body: JSON.stringify({ transactionId: transactionId }),
    }).then((_res) => {
        document.location.reload(true)
    })
}

// Track current page route
let currentPage = window.location.pathname

// Apply right functionality
if (currentPage == '/transactions') {
    dropdownMenu('filter')
    dropdownMenu('months')
    dropdownMenu('years')

    // Drop down table on smaller screens
    const TABLE_TOGGLE = document.querySelectorAll('.transactions-table tr')
    TABLE_TOGGLE.forEach(row => {
        row.addEventListener('click', () => {
            row.classList.toggle('active')
        })
    })


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
        document.querySelectorAll('input[name="category"]').forEach(radioButton => {
            radioButton.checked = false
        })
    })
}
