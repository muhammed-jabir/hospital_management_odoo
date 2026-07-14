gsap.registerPlugin(ScrollTrigger);
gsap.registerPlugin(Flip);

let flipCtx;

function createTween() {
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

        return () => gsap.set(galleryItems, { clearProps: "all" });
    });
}

function initGallery() {
    createTween();
    window.addEventListener("resize", createTween);
}

if (document.readyState === "complete") {
    initGallery();
} else {
    window.addEventListener("load", initGallery);
}