function uploadImg() {
    const cloudName = 'dzhpku2a7';
    const unsignedUploadPreset = 'tmrndy21';
    let url = `https://api.cloudinary.com/v1_1/${cloudName}/upload`;

    let file = document.querySelector("#fileSelect").files[0];

    const formData = new FormData();
    formData.append('file', file);
    formData.append('upload_preset', unsignedUploadPreset);

    fetch(url, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then((data) => {
      if (data.secure_url !== '') {
          const uploadedFileUrl = data.secure_url;

        // document.querySelector("#cl_img").setAttribute("src", uploadedFileUrl);
          // document.getElementById("addRecipeForm").submit();
          document.createElement('form').submit.call(document.addRecipeForm);
      }
    })
    .catch(err => console.error(err));
}

document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.includes("modify_recipe") == false) {
        console.log("not modify_recipe"); return;
    }
    // const fileSelect = document.querySelector("#fileSelect");
    const addRecipeForm = document.querySelector("#addRecipeForm");

    // fileSelect.addEventListener('change', (e) => {
    //     uploadImg(e);
    // });

    addRecipeForm.addEventListener('submit', (e) => {
        e.preventDefault();
        uploadImg();
    })
});
