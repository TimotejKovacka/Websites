let cards = document.getElementsByClassName("card");

Array.from(cards).forEach((card) => {
    card.addEventListener("click", () => {
        card.classList.toggle("card--flipped");
    })
})