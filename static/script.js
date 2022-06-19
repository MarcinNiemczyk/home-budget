// Navbar toggle
const NAVBAR = document.querySelector('nav')

document.querySelector('.toggle-menu').addEventListener('click', () => {
    NAVBAR.classList.add('active')
})

document.querySelector('.navbar__close').addEventListener('click', () => {
    NAVBAR.classList.remove('active')
})


// Category dropdown menu
const SELECTED_CATEGORY = document.querySelector('.category__selected')
const CATEGORY_CONTAINER = document.querySelector('.category')
const CATEGORY = document.querySelectorAll('.category__option label')

// Toggle visibility of dropdown menu
SELECTED_CATEGORY.addEventListener('click', () => {
    CATEGORY_CONTAINER.classList.toggle('active')
})

CATEGORY.forEach(option => {
    option.addEventListener('click', () => {
        // Change selected category value
        SELECTED_CATEGORY.innerHTML = option.innerHTML

        // Remove active style effect from previous option
        CATEGORY.forEach(option => {
            option.classList.remove('active')
        })
        
        // Add active style effect to new option
        option.classList.add('active')

        // Close dropdown menu
        CATEGORY_CONTAINER.classList.remove('active')
    })
})

// Filter dropdown menu
const SELECTED_FILTER = document.querySelector('.filter__selected')
const FILTER_CONTAINER = document.querySelector('.filter')
const FILTER = document.querySelectorAll('.filter__option label')

// Toggle visibility of dropdown menu
SELECTED_FILTER.addEventListener('click', () => {
    FILTER_CONTAINER.classList.toggle('active')
})

FILTER.forEach(option => {
    option.addEventListener('click', () => {
        // Change selected filter value
        SELECTED_FILTER.innerHTML = option.innerHTML

        // Remove active style effect from previous option
        FILTER.forEach(option => {
            option.classList.remove('active')
        })
        
        // Add active style effect to new option
        option.classList.add('active')

        // Close dropdown menu
        FILTER_CONTAINER.classList.remove('active')
    })
})


// const FILTERS = document.querySelectorAll('input[name="filter__radio"]')

// FILTERS.forEach(filter => {
//     filter.addEventListener('change', () => {
//         if (filter.checked) {
//             console.log(filter.value + ' is checked')
//         }
//     })
// })


// Months dropdown menu
const SELECTED_MONTH = document.querySelector('.months__selected')
const MONTHS_CONTAINER = document.querySelector('.months')
const MONTHS = document.querySelectorAll('.months__option label')

// Toggle visibility of months dropdown menu
SELECTED_MONTH.addEventListener('click', () => {
    MONTHS_CONTAINER.classList.toggle('active')
})

MONTHS.forEach(option => {
    option.addEventListener('click', () => {
        // Change selected month value
        SELECTED_MONTH.innerHTML = option.innerHTML

        // Remove active style effect from previous option
        MONTHS.forEach(option => {
            option.classList.remove('active')
        })
        
        // Add active style effect to new option
        option.classList.add('active')

        // Close dropdown menu
        MONTHS_CONTAINER.classList.remove('active')
    })
})

// Years dropdown menu
const SELECTED_YEAR = document.querySelector('.years__selected')
const YEARS_CONTAINER = document.querySelector('.years')
const YEARS = document.querySelectorAll('.years__option label')

// Toggle visibility of months dropdown menu
SELECTED_YEAR.addEventListener('click', () => {
    YEARS_CONTAINER.classList.toggle('active')
})

YEARS.forEach(option => {
    option.addEventListener('click', () => {
        // Change selected month value
        SELECTED_YEAR.innerHTML = option.innerHTML

        // Remove active style effect from previous option
        YEARS.forEach(option => {
            option.classList.remove('active')
        })
        
        // Add active style effect to new option
        option.classList.add('active')

        // Close dropdown menu
        YEARS_CONTAINER.classList.remove('active')
    })
})
