document.addEventListener("DOMContentLoaded",()=>{


const dot=document.createElement("div");
dot.className="cursor-dot";


const outline=document.createElement("div");
outline.className="cursor-outline";


document.body.appendChild(dot);
document.body.appendChild(outline);



window.addEventListener("mousemove",(e)=>{


dot.style.left=e.clientX+"px";
dot.style.top=e.clientY+"px";


outline.style.left=e.clientX-20+"px";
outline.style.top=e.clientY-20+"px";


});


document.querySelectorAll("a,button,.card")
.forEach(el=>{


el.addEventListener("mouseenter",()=>{

outline.style.transform="scale(1.8)";

});


el.addEventListener("mouseleave",()=>{

outline.style.transform="scale(1)";

});


});


});