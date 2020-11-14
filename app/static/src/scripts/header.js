document.addEventListener('DOMContentLoaded', () => {
    let toggler = document.querySelector("#headerToggler");

    if (toggler) {
        toggler.addEventListener("click", (e) => {
            let nav = document.querySelector("#mobileNav");
            nav.classList.toggle("hidden");

            e.target.classList.toggle("toggler_open");
            e.target.classList.toggle("toggler_close");
        });
    }
});
