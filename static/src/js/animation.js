let flipCtx; // must be declared at module scope, before createGalleryTween uses it

function initSiteAnimation() {

    if (!window.gsap || !window.Flip || !window.ScrollTrigger) {
        console.log("GSAP not loaded yet");
        setTimeout(initSiteAnimation, 100);
        return;
    }

    gsap.registerPlugin(Flip, ScrollTrigger);
    initFlipmodal();
    initFlipCarousel();
    initScrollAnimations();
    initFlipGallery();
    initNewAnimation();

    ScrollTrigger.refresh();
}

function initFlipmodal() {
    const modal = document.querySelector(".album-modal");
    if (!modal) {
        console.log("modal not found");
        return; // was falling through to modal.querySelector() on null before
    }
    const modalContent = modal.querySelector(".content");
    const modalOverlay = modal.querySelector(".overlay");
    const boxes = gsap.utils.toArray(".album-boxes-container .album-box");
    const boxesContent = gsap.utils.toArray(".album-box-content");
    let boxIndex = undefined;

    boxesContent.forEach((box, i) => {
        box.addEventListener("click", () => {
            if (boxIndex !== undefined) {
                const state = Flip.getState(box);
                boxes[boxIndex].appendChild(box);
                boxIndex = undefined;
                gsap.to([modal, modalOverlay], {
                    autoAlpha: 0,
                    ease: "power1.inOut",
                    duration: 0.35
                });
                Flip.from(state, {
                    duration: 0.7,
                    ease: "power1.inOut",
                    absolute: true,
                    onComplete: () => gsap.set(box, {zIndex: "auto"})
                });
                gsap.set(box, {zIndex: 1002});
            } else {
                const state = Flip.getState(box);
                modalContent.appendChild(box);
                boxIndex = i;
                gsap.set(modal, {autoAlpha: 1});
                Flip.from(state, {
                    duration: 0.7,
                    ease: "power1.inOut"
                });
                gsap.to(modalOverlay, {autoAlpha: 0.65, duration: 0.35});
            }
        });
    });
}

function initFlipCarousel() {
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
            duration: 0.8,
            ease: "power2.inOut",
            simple: true,
            onEnter: (elements) => {
                gsap.set(elements, {zIndex: 20});
            },
            onLeave: (elements) => {
                gsap.set(elements, {zIndex: 20});
            },
            onComplete: () => {
                isAnimating = false;
            }
        });
    }

    startAutoplay();
}

function initFlipGallery() {
    createGalleryTween();
    window.addEventListener("resize", createGalleryTween);
}

function createGalleryTween() {
    const galleryElement = document.querySelector("#gallery-8");
    if (!galleryElement) return;

    const galleryItems = galleryElement.querySelectorAll(".gallery__item");
    if (!galleryItems.length) return;

    if (flipCtx) flipCtx.revert();
    galleryElement.classList.remove("gallery--final");

    flipCtx = gsap.context(() => {
        galleryElement.classList.add("gallery--final");
        const flipState = Flip.getState(galleryItems);
        galleryElement.classList.remove("gallery--final");

        const flip = Flip.to(flipState, {
            simple: true,
            ease: "expoScale(1, 5)"
        });

        const tl = gsap.timeline({
            scrollTrigger: {
                trigger: galleryElement,
                start: "center center",
                end: "+=100%",
                scrub: true,
                pin: true
            }
        });
        tl.add(flip);

        return () => gsap.set(galleryItems, {clearProps: "all"});
    });
}

function initScrollAnimations() {
    gsap.from(".hero-title", {y: 80, opacity: 0, duration: 1});

    if (document.querySelector(".gallery-section")) {
        gsap.from(".gallery-section", {
            scrollTrigger: {
                trigger: ".gallery-section",
                start: "top 75%"
            },
            opacity: 0,
            scale: 0.9
        });
    }

    gsap.from(
        ".carousel-section",
        {opacity: 0, y: 80},
        {
            opacity: 1,
            y: 0,
            duration: 0.8,
            scrollTrigger: {trigger: ".carousel-section", start: "top 80%"}
        }
    );

    gsap.from(
        ".doctor-section",
        {opacity: 0, y: 80},
        {
            opacity: 1,
            y: 0,
            duration: 0.8,
            stagger: 0.15,
            scrollTrigger: {trigger: ".doctor-section", start: "top 80%"}
        }
    );

    gsap.from(
        ".service-section",
        {opacity: 0, y: 80},
        {
            opacity: 1,
            y: 0,
            duration: 0.8,
            stagger: 0.2,
            scrollTrigger: {trigger: ".service-section", start: "top 80%"}
        }
    );
}

function initNewAnimation(){
    gsap.utils.toArray("[data-animation]")
    .forEach(card=>{


    gsap.from(card,{

    scrollTrigger:{
    trigger:card,
    start:"top 85%"
    },

    opacity:0,

    y:80,

    duration:1

    })


})
}



if (document.readyState === "complete") {
    initSiteAnimation();
} else {
    window.addEventListener("load", initSiteAnimation);
}