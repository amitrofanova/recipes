function uploadImg(e) {
    const cloudName = 'dzhpku2a7';
    const unsignedUploadPreset = 'tmrndy21';
    let url = `https://api.cloudinary.com/v1_1/${cloudName}/upload`;

    const file = e.target.files[0];
    console.log(file);
    const formData = new FormData();

    let img = document.querySelector("#fileSelect").files[0];
        console.log(img);

    formData.append('file', file);
    formData.append('upload_preset', unsignedUploadPreset);

    // fetch(url, {
    //     method: 'POST',
    //     body: formData,
    // })
    // .then(response => response.json())
    // .then((data) => {
    //   if (data.secure_url !== '') {
    //     const uploadedFileUrl = data.secure_url;
    //
    //     document.querySelector("#cl_img").setAttribute("src", uploadedFileUrl);
    //   }
    // })
    // .catch(err => console.error(err));
}

document.addEventListener('DOMContentLoaded', () => {
    const fileSelect = document.querySelector("#fileSelect");
    const addRecipeForm = document.querySelector("#addRecipeForm");

    fileSelect.addEventListener('change', (e) => {
        uploadImg(e);
    });

    // addRecipeForm.addEventListener('submit', (e) => {
    //     let img = document.querySelector("#fileSelect").files[0];
    //     console.log(img);
    // })
});
