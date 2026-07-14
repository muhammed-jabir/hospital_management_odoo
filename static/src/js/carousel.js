function initFlipCarousel() {
  gsap.registerPlugin(Flip,ScrollTrigger);

  

  const container = document.querySelector(".flip-container");
  const nextBtn = document.getElementById("next");
  const prevBtn = document.getElementById("prev");
  if (!container || !nextBtn || !prevBtn) {
    console.log("Carousel elements not found");
    return;
  }

  let isAnimating = false;
  let autoplayTimer = null;
  const AUTOPLAY_DELAY = 3000;

  function startAutoplay() {
    stopAutoplay();
    autoplayTimer = setInterval(() => {
      if (!isAnimating) {
        updateCaterpillar(true);
      }
    }, AUTOPLAY_DELAY);
  }

  function stopAutoplay() {
    if (autoplayTimer) clearInterval(autoplayTimer);
  }

  nextBtn.addEventListener("click", () => {
    if (isAnimating) return;
    isAnimating = true;
    updateCaterpillar(true);
    startAutoplay();
  });

  prevBtn.addEventListener("click", () => {
    if (isAnimating) return;
    isAnimating = true;
    updateCaterpillar(false);
    startAutoplay();
  });

  function updateCaterpillar(forward) {

    const cards = gsap.utils.toArray(".flip-container img");

    const first = cards[0];
    const last = cards[cards.length - 1];

    const state = Flip.getState(cards);


    if (forward) {

        container.appendChild(first);

    } else {

        container.insertBefore(last, first);

    }


    Flip.from(state, {
    duration:0.8,
    ease:"power2.inOut",
    simple:true,

    onEnter:(elements)=>{
        gsap.set(elements,{
            zIndex:20
        });
    },

    onLeave:(elements)=>{
        gsap.set(elements,{
            zIndex:20
        });
    },

    onComplete:()=>{
        isAnimating=false;
    }
});

}

  startAutoplay();
}

if (document.readyState === "complete") {
    initFlipCarousel();
} else {
    window.addEventListener("load", initFlipCarousel);
}
