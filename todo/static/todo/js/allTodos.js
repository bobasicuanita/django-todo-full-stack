const deleteButtons = document.querySelectorAll(".delete-button");
const modal = document.querySelector("#delete-modal");
const cancelBtn = document.querySelector("#cancel-delete");
const deleteForm = document.querySelector("#confirm-delete-form");

// Modal
deleteButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const deleteUrl = button.dataset.deleteUrl;
        deleteForm.action = deleteUrl;
        modal.classList.remove("hidden");
    });
});

cancelBtn.addEventListener("click", () => {
    modal.classList.add("hidden");
});


// Filters
const all = document.querySelector('#all')
const marked_done = document.querySelector('.filter-pill--marked_done')
const pending = document.querySelector('.filter-pill--pending')
const overdue = document.querySelector('.filter-pill--overdue')
const high = document.querySelector('.filter-pill--high')
const medium = document.querySelector('.filter-pill--medium')
const low = document.querySelector('.filter-pill--low')

const urgencyChoices = {
    high: high,
    medium: medium,
    low: low,
};

const searchParams = new URLSearchParams(window.location.search);

if (searchParams.size === 0) {
    all.classList.add("filter-pill--active");
} else {
    const [filter, value] = searchParams.entries().next().value;

    if (filter === "marked_done") {
        if (value === true) {
            marked_done.classList.add("filter-pill--active");
        } else {
            pending.classList.add("filter-pill--active");
        }
    }

    if (filter === "is_overdue") {
        overdue.classList.add("filter-pill--active");
    }

    if (filter === "urgency") {
        urgencyChoices[value].classList.add("filter-pill--active");
    }
}