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

// Drop down table on smaller screens
function tableToggle(tr) {
    tr.forEach(row => {
        row.addEventListener('click', () => {
            row.classList.toggle('active')
        })
    })
}


// Track current page route
let currentPage = window.location.pathname

// Ensure script is running on right page
if (currentPage.includes('/transactions')) {
    if (currentPage == '/transactions/add') {
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
    dropdownMenu('filter')
    dropdownMenu('months')
    dropdownMenu('years')

    let tr = document.querySelectorAll('.transactions-table tr')
    tableToggle(tr)

    // Handle search bar
    let input = document.querySelector('.search__input')
    input.addEventListener('input', async function() {
        // Send request with current transaction page to keep track of filters
        let response = await fetch(currentPage + '?q=' + input.value)
        let transactions = await response.json()
        let html = ''
        // Replace html tags inside tbody
        for (let id in transactions) {
            html += '<tr><td data-label="Date">' + transactions[id].date + '</td>'
            html += '<td data-label="Name"><i class="table-drop fa-solid fa-circle-chevron-down"></i>' + transactions[id].name + '</td>'
            html += '<td data-label="Type">' + transactions[id].type + '</td>'
            html += '<td data-label="Amount">' + transactions[id].amount + '$</td>'
            html += '<td data-label="Category">' + transactions[id].category + '</td>'
            html += '<td data-label="Action"><i class="table-remove fa-solid fa-trash-can" onclick="removeTransaction(' + transactions[id].id + ')"></i></td></tr>'
        }
        document.querySelector('tbody').innerHTML = html
        // Handle dropdown table on smaller screen for new table rows
        tr = document.querySelectorAll('.transactions-table tr')
        tableToggle(tr)
    })
} else if (currentPage.includes('/planning')) {
    dropdownMenu('months')
    dropdownMenu('years')
}
