console.clear();
gsap.registerPlugin(Flip);

const container = document.querySelector(".container");
const cards = gsap.utils.toArray("img", container);
const nextBtn = document.getElementById("next");
const prevBtn = document.getElementById("prev");
let isAnimating = false;

nextBtn.addEventListener("click", () => {
  if (isAnimating) return;
  isAnimating = true;
  updateCaterpillar(true);
});
prevBtn.addEventListener("click", () => {
  if (isAnimating) return;
  isAnimating = true;
  updateCaterpillar(false);
});

const updateCaterpillar = (forward) => {
  const cards = gsap.utils.toArray("img", container);
  const first = cards[0];
  const last = cards[cards.length - 1];
  const state = Flip.getState(cards);
  let newCard = document.createElement("img");
  gsap.set(newCard, { scale: 0, opacity: 0 });

  if (forward) {
    newCard.src = first.src;
    container.append(newCard);
    first.classList.add("hide");
  } else {
    newCard.src = last.src;
    newCard.innerText = last.innerText;
    container.prepend(newCard);
    last.classList.add("hide");
  }
  Flip.from(state, {
    targets: "img",
    fade: true,
    absoluteOnLeave: true,
    onEnter: (els) => {
      gsap.to(els, {
        opacity: 1,
        scale: 1,
        transformOrigin: forward ? "bottom right" : "bottom left"
      });
    },
    onLeave: (els) => {
      gsap.to(els, {
        opacity: 0,
        scale: 0,
        transformOrigin: forward ? "bottom left" : "bottom right",
        onComplete: () => {
          els[0].remove();
          isAnimating = false;
        }
      });
    }
  });
};
