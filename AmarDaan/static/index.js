// main.js

// Code for changing header image
const headerImage = document.getElementById("headerImage");

let currentImageIndex = 0;

function changeImage() {
  currentImageIndex = (currentImageIndex + 1) % imageSources.length;
  headerImage.src = imageSources[currentImageIndex];
}

setInterval(changeImage, 2500);

// Code for campaign cards
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const cardRow = document.getElementById("cardRow");



let startIndex = 0;
const cardsPerRow = 4;

prevBtn.addEventListener("click", () => {
  startIndex = Math.max(startIndex - cardsPerRow, 0);
  updateCards();
});

nextBtn.addEventListener("click", () => {
  startIndex = Math.min(startIndex + cardsPerRow, campaignData.length - cardsPerRow);
  updateCards();
});

function updateCards() {
    const endIndex = startIndex + cardsPerRow;
    cardRow.innerHTML = "";

    for (let i = startIndex; i < endIndex; i++) {
      if (i >= campaignData.length) {
        break;
      }

      const progressPercentage = (campaignData[i].collected / campaignData[i].budget) * 100;

      const card = document.createElement("div");
      card.className = "col";
      card.innerHTML = `
      <div class="card shadow" style="border: 0px;">
      <img src="${campaignData[i].imageUrl}" class="card-img-top img-fluid" style="height: 300px;" alt="Campaign Image">
      <div class="card-body" >
        <h5 class="card-title">${campaignData[i].name}</h5>
        <p class="card-text">Target Budget: $${campaignData[i].budget}</p>
        <div class="progress mb-3">
          <div class="progress-bar" role="progressbar" style="width: ${progressPercentage}%" aria-valuenow="${progressPercentage}" aria-valuemin="0" aria-valuemax="100">
            $${campaignData[i].collected} / $${campaignData[i].budget}
          </div>
        </div>
        <button class="btn btn-primary">View Details</button>
      </div>
    </div>
    
      `;

      cardRow.appendChild(card);
    }
  }

updateCards();

// Code for sign-up/sign-in buttons
const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});


