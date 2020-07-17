import '../styles/desktop.scss';

async function deleteIdea(event) {
    let selectedIdeaNum = event.target.getAttribute("data-id");
    let url = window.location.pathname;

    let response = await fetch(url, {
        method: 'DELETE',
        body: selectedIdeaNum
    });

    if (response.ok) {
        location.reload();
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    let deleteIdeaBtns = document.querySelectorAll("#ideas button");

    Array.from(deleteIdeaBtns).forEach((btn) => {
        btn.addEventListener("click", () => {
                deleteIdea(event);
            }
        );
    });
});
