async function processImg() {
    const cloudName = 'dzhpku2a7';
    const unsignedUploadPreset = 'tmrndy21';
    let url = `https://api.cloudinary.com/v1_1/${cloudName}/upload`;
    let file = document.querySelector("#fileSelect").files[0];

    const formData = new FormData();
    formData.append('file', file);
    formData.append('upload_preset', unsignedUploadPreset);

    let uploadToCloudinary = await fetch(url, {
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
