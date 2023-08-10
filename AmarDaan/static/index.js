// JavaScript code here
const headerImage = document.getElementById("headerImage");
const imageSources = [
  "./resources/images/header-img-1.jpg",
  "./resources/images/header-img-3.jpg",
  "./resources/images/header-img-4.jpg",
  "./resources/images/header-img-5.jpg",
  "./resources/images/header-img-6.jpg"
];

let currentImageIndex = 0;

function changeImage() {
  currentImageIndex = (currentImageIndex + 1) % imageSources.length;
  headerImage.src = imageSources[currentImageIndex];
}

setInterval(changeImage, 3000);

const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const cardRow = document.getElementById("cardRow");

const campaignData = [
  // Your campaign data objects here
];

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
// JavaScript code here
// ...

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
        <div class="card">
          <img src="${campaignData[i].imageUrl}" class="card-img-top" alt="Campaign Image">
          <div class="card-body">
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
  