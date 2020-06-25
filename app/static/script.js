//document.addEventListener('DOMContentLoaded', function() {
//    document.querySelector('button').onclick = deleteIdea;
//});

//var container = document.querySelector("#ideas");
//var ideas = container.querySelectorAll("button");


async function deleteIdea(event) {
    var selectedIdeaNum = event.target.getAttribute("data-id");
//    var url = '/try_new';
    var url = window.location.pathname;

    let response = await fetch(url, {
        method: 'DELETE',
        body: selectedIdeaNum
    });

    if (response.ok) {
//        await location.reload();
        location.reload();
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
}

var deleteIdeaBtns = document.querySelectorAll("#ideas button");

Array.from(deleteIdeaBtns).forEach((btn) => {
    btn.addEventListener("click", () => {
            deleteIdea(event);
        }
    );
});
