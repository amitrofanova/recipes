function deleteIdea(event) {
    var selectedIdeaNum = event.target.getAttribute("data-id");
    var hToChange = selectedIdeaNum + "h";

    console.log(selectedIdeaNum);
    console.log(document.querySelector(`h1[data-id="${selectedIdeaNum}h"]`));
    document.querySelector(`h1[data-id="${selectedIdeaNum}h"]`).innerHTML = "new";
}

//document.addEventListener('DOMContentLoaded', function() {
//    document.querySelector('button').onclick = deleteIdea;
//});

//var container = document.querySelector("#ideas");
//var ideas = container.querySelectorAll("button");



function deleteData(event) {
    var selectedIdeaNum = event.target.getAttribute("data-id");
    var url = '/try_new';

    return fetch(url, {
        method: 'delete',
        body: selectedIdeaNum
    })
    .then(response => response.text());
}


var deleteIdeaBtns = document.querySelectorAll("#ideas button");

Array.from(deleteIdeaBtns).forEach((btn) => {
    btn.addEventListener("click", () => {
        deleteData(event)
            .then(data => console.log(data));
        }
    );
});
