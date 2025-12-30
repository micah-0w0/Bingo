function ballRoll() {
    const sound = document.getElementById("roll_sound");
    sound.currentTime = 0;
    sound.play();

    // Redirect after sound starts
    setTimeout(() => {
        window.location.href = "/roll";
    }, 2000);
}

function enableBingoClicks() {
    const cells = document.querySelectorAll(".bingo-board td");
    const sound = document.getElementById("tap_sound");
    sound.currentTime = 0;

    cells.forEach(cell => {
        cell.addEventListener("click", () => {
            sound.play();
            cell.classList.toggle("selected");
            cell.classList.toggle("not-selected");
        });
    });
}

function setupPopup(openButtonId, popupId, closeButtonId) {
  const popup = document.getElementById(popupId);
  const openBtn = document.getElementById(openButtonId);
  const closeBtn = document.getElementById(closeButtonId);

  openBtn.onclick = () => popup.style.display = "flex";
  closeBtn.onclick = () => popup.style.display = "none";

  window.onclick = (e) => {
    if (e.target === popup) popup.style.display = "none";
  };
}

function openCheckPopup() {
    const modal = document.getElementById("checkModal");
    modal.style.display = "flex";

    const form = document.getElementById("checkForm");
    form.onsubmit = (e) => {
        e.preventDefault();

        const pid = document.getElementById("playerInput").value;
        const bid = document.getElementById("boardInput").value;

        // Redirect to /check
        window.location.href = `/check?player_id=${pid}&board_id=${bid}`;
    };
}

document.addEventListener("DOMContentLoaded", () => {
    enableBingoClicks();
    setupPopup("bingo-button", "popup", "closePopup");
});
