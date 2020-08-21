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

function toggleClass() {
    let ideasMain = document.querySelector("#ideasMain");
    let screenWidth = screen.width;
    console.log(screenWidth);

    if (screenWidth > 600) {
        ideasMain.classList.remove("flex-direction_column-reverse");
        ideasMain.classList.add("justify-content_space-between");
    } else {
        ideasMain.classList.remove("justify-content_space-between");
        ideasMain.classList.add("flex-direction_column-reverse");
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

    toggleClass();
    window.onresize = toggleClass();
});
