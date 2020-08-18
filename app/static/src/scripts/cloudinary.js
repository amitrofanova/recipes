import { createLoader, destroyLoader } from "./loader.js";

// https://stackoverflow.com/questions/43792026/display-spinner-during-ajax-call-when-using-fetch-api/43792214
// Store a copy of the fetch function
var _oldFetch = fetch;

// Create our new version of the fetch function
window.fetch = function(){

    // Create hooks
    var fetchStart = new Event( 'fetchStart', { 'view': document, 'bubbles': true, 'cancelable': false } );
    var fetchEnd = new Event( 'fetchEnd', { 'view': document, 'bubbles': true, 'cancelable': false } );

    // Pass the supplied arguments to the real fetch function
    var fetchCall = _oldFetch.apply(this, arguments);

    // Trigger the fetchStart event
    document.dispatchEvent(fetchStart);

    fetchCall.then(function(){
        // Trigger the fetchEnd event
        document.dispatchEvent(fetchEnd);
    }).catch(function(){
        // Trigger the fetchEnd event
        document.dispatchEvent(fetchEnd);
    });

    return fetchCall;
};

async function processImg() {
    const cloudName = 'dzhpku2a7';
    const unsignedUploadPreset = 'tmrndy21';
    let url = `https://api.cloudinary.com/v1_1/${cloudName}/upload`;
    let file = document.querySelector("#fileSelect").files[0];

    const formData = new FormData();
    formData.append('file', file);
    formData.append('upload_preset', unsignedUploadPreset);

    let uploadToCloudinary = await window.fetch(url, {
        method: 'POST',
        body: formData,
    });

    let cloudinaryData = await uploadToCloudinary.json();
    document.querySelector('#image_url').value = cloudinaryData.secure_url;

    await new Promise((resolve, reject) => {
        document.querySelector('#image_url').value = cloudinaryData.secure_url;
        document.createElement('form').submit.call(document.addRecipeForm);
    });

    return sendDataToServer;
}

document.addEventListener('DOMContentLoaded', () => {
    if (!window.location.pathname.includes("modify_recipe") &&
        !window.location.pathname.includes("add_recipe")) return;

    const fileSelect = document.querySelector('#fileSelect');
    fileSelect.addEventListener('change', (e) => {
        document.querySelector('#fileName').innerHTML = e.target.files[0].name;
    });

    document.addEventListener('fetchStart', function() {
        console.log("fetch start");
        createLoader("Пожалуйста подождите, рецепт сохраняется");
    });

    document.addEventListener('fetchEnd', function() {
        console.log("Hide spinner");
    });

    const addRecipeForm = document.querySelector('#addRecipeForm');
    addRecipeForm.addEventListener('submit', (e) => {
        e.preventDefault();
        processImg();
    });

    if (window.location.pathname.includes("modify_recipe")) {
        let imgUrl = document.querySelector("#image_url").value;
        document.querySelector("#imgPreview").src = imgUrl;
    }
});
