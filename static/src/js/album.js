
function initFlipmodal() {
    gsap.registerPlugin(Flip);

    const modal = document.querySelector(".album-modal");
    if (!modal){
        console.log('model not found')
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
if (document.readyState==="complete") {
    initFlipmodal();
}else{
    window.addEventListener("load",initFlipmodal);
}
