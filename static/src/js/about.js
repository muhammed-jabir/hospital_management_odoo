function initAboutAnimation(){


    console.log(
        "About animation started"
    );
    gsap.registerPlugin(
        ScrollTrigger
    );

    const panels =
        gsap.utils.toArray(
            ".slides-wrapper > .about-section"
        );

    console.log(
        "Panels found:",
        panels.length
    );

    panels.forEach((panel, index)=>{

    console.log(
        "Creating trigger for panel:",
        index
    );

    const innerpanel =
        panel.querySelector(
            ".about-section-inner"
        );

    if(!innerpanel){

            console.log(
                "No inner panel"
            );
            return;
    }

    let panelHeight =
        innerpanel.offsetHeight;

    let windowHeight =
        window.innerHeight;


    let difference =
            panelHeight - windowHeight;

    let fakeScrollRatio =
            difference > 0
            ?
            difference /
            (difference + windowHeight)
            :
            0;

    if(fakeScrollRatio){
        panel.style.marginBottom = panelHeight *
            fakeScrollRatio +
            "px";
    }

    let timeline =
            gsap.timeline({

                scrollTrigger:{
                    trigger: panel,
                    start: "top top",
                    end: "+=100%",
                    pin:true,
                    scrub:1,
                    pinSpacing:true,
                    markers:true

                }

            });

    if(fakeScrollRatio){
            timeline.to(
                innerpanel,
                {
                    yPercent:-100,
                    y:windowHeight,
                    ease:"none"
                });
    }

    timeline
        .to(
            panel,
            {
                scale:0.7,
                opacity:0.5,
                duration:0.9
            })
        .to(
            panel,
            {
                opacity:0,
                duration:0.1
            }
        );
    });
    window.addEventListener("load", () => {
    ScrollTrigger.refresh();});

    console.log(
        "Triggers:",
        ScrollTrigger.getAll()
    );
}

function waitForGSAP(){
    if(
        window.gsap &&
        window.ScrollTrigger
    ){
        initAboutAnimation();
    }
    else{
        setTimeout(
            waitForGSAP,
            100
        );
    }
}
waitForGSAP();

