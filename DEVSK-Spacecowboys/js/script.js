function scrollToSection(section) {
    $([document.documentElement, document.body]).animate({
        scrollTop: $(section).offset().top
    }, 750);
    $("#nav-toggle").prop("checked", false);
    $("#nav-toggle")[0].labels[0].children[0].innerHTML = "MENU";
}

function findAncestor (el, cls) {
    while ((el = el.parentElement) && !el.classList.contains(cls));
    return el;
}

function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function errorIndicator(emailForm, index) {
    emailForm[index].parentNode.classList.remove("valid");
    emailForm[index].parentNode.classList.add("invalid");
    emailForm.children[0].children[index*2].classList.add("error");
    emailForm.children[0].children[index*2].style.display = "block";
    emailForm.children[0].children[index*2+1].children[1].classList.add("flexible", "error");
    emailForm.children[0].children[index*2+1].children[1].classList.remove("valid");
    emailForm.children[0].children[index*2+1].children[1].children[0].classList.remove("visible");
    emailForm.children[0].children[index*2+1].children[1].children[1].classList.add("visible")
}

function validIndicator(emailForm, index) {
    emailForm[index].parentNode.classList.add("valid");
    emailForm.children[0].children[index*2+1].children[1].classList.add("valid", "flexible");
    emailForm.children[0].children[index*2+1].children[1].classList.remove("error");
    emailForm.children[0].children[index*2+1].children[1].children[0].classList.add("visible");
    emailForm.children[0].children[index*2+1].children[1].children[1].classList.remove("visible");
}

let carousel = {
    plusIndex: function(object, n) {
        if (object.index === object.max) {
            object.index = object.min;
        } else {
            object.index += n
        }
        return object.index
    },
    minusIndex: function(object, n) {
        if (object.index === object.min) {
            object.index = object.max;
        } else {
            object.index -= n
        }
        return object.index
    }
};
let lightBox = {
        index: 2,
        max: 12,
        min: 1,
        changeImg: function() {
            $(".showcase img")[0].attributes[0].value = "/images/"+this.index+".png";
        }
    },
    slideShow = {
        children: document.getElementsByClassName("person-card"),
        index: 2,
        max: 5,
        min: 1,
        
        changeSlide: function() {
            for (let i=1; i < this.children.length+1;i++){
                $(".person-card-nav")[0].children[i].classList.remove("active");
            }
            this.children[this.index-1].scrollIntoView({behavior: "smooth", block: "center", inline: "center"});
            $(".person-card-nav")[0].children[this.index].classList.add("active");
        }
    };

$(document).ready(function() {
    var emailForm = document.getElementById("email-form"),
        firstNameInput = document.getElementById("first-name"),
        lastNameInput = document.getElementById("last-name"),
        emailInput = document.getElementById("email"),
        aboutUsY = $(".about-us").offset().top,
        teamY = $(".team").offset().top,
        starsY = $(".stars").offset().top,
        contactUsY = $(".contact-us").offset().top,
        lastScrollTop = 0;

    $("#nav-toggle").change(function() {
        if(this.checked) {
            $("nav").height($(".hero").height()).css({
                backgroundColor: "#161B20"
            });
            if($(window).scrollTop() != 0){
                $("header").css({
                    opacity: "1"
                });
            }
            this.labels[0].children[0].innerHTML = "<span class="+"material-icons"+">close</span> CLOSE";
        } else {
            if($(window).scrollTop() != 0){
                $("header").css({
                    backgroundColor: "#484D52",
                    opacity: "0.9"
                })
            }
            this.labels[0].children[0].innerHTML = "MENU";
        }
    });

    $(".person-card").click(function(event) {
        let personCard = findAncestor(event.target, "person-card"),
            personCardArr = personCard.classList;

        if(personCardArr.length>1){
            personCard.classList.remove("flipped");
        } else {
            personCard.classList.add("flipped");
        }
        
    })
    $(window).scroll(function() {
        let windowLocation = window.pageYOffset + window.innerHeight / 2;
        if($(this).scrollTop() != 0 && lastScrollTop<=$(this).scrollTop()) {
            if(document.getElementById("nav-toggle").checked){}
            else{
                $("header").css({
                    backgroundColor: "#484D52",
                    opacity: "0.9"
                })
            }
            if( aboutUsY <= windowLocation && windowLocation <= teamY) {
                $("nav li a").css("color", "");
                $("nav li:nth-child(1) a").css("color", "#FFDC08");
            } else if (teamY <= windowLocation && windowLocation <= starsY) {
                $("nav li a").css("color", "");
                $("nav li:nth-child(2) a").css("color", "#FFDC08");
            } else if (starsY <= windowLocation && windowLocation <= contactUsY) {
                $("nav li a").css("color", "");
                $("nav li:nth-child(3) a").css("color", "#FFDC08");
            } else if (contactUsY <= windowLocation ) {
                $("nav li a").css("color", "");
                $("nav li:nth-child(4) a").css("color", "#FFDC08");
            } else {
                $("nav li a").css("color", "");
            }
        } else {
            if(! $("#nav-toggle")[0].checked){
                $("header").css({
                    opacity: "0"
                });
            }
        }
        if(window.pageYOffset === 0){
            $("header").css({
                opacity: "1",
                backgroundColor: ""
            });
        }
        lastScrollTop = $(this).scrollTop();
    });

    $("#learn-more").click(function(){
        $([document.documentElement, document.body]).animate({
            scrollTop: $(".about-us").offset().top
        }, 750);
    });

    $("nav li:nth-child(1) a").click(function(e){
        e.preventDefault();
        scrollToSection(".about-us");
    });
    $("nav li:nth-child(2) a").click(function(e){
        e.preventDefault();
        scrollToSection(".team");
    });
    $("nav li:nth-child(3) a").click(function(e){
        e.preventDefault();
        scrollToSection(".stars");
    });
    $("nav li:nth-child(4) a").click(function(e){
        e.preventDefault();
        scrollToSection(".contact-us");
    });
    var helpTextArr = document.getElementsByClassName("help-text");

    firstNameInput.addEventListener("invalid", function(event) {
        event.preventDefault();
    });
    lastNameInput.addEventListener("invalid", function(event) {
        event.preventDefault();
    });
    emailInput.addEventListener("invalid", function(event) {
        event.preventDefault();
    });
    firstNameInput.addEventListener("input", function(event) {
        if (helpTextArr[0].style.display === "block") {
            firstNameInput.parentNode.classList.remove("invalid");
            helpTextArr[0].style.display = "none";
            emailForm.children[0].children[0*2+1].children[1].classList.remove("flexible");
        }
    });
    lastNameInput.addEventListener("input", function(event) {
        if (helpTextArr[1].style.display === "block") {
            lastNameInput.parentNode.classList.remove("invalid");
            helpTextArr[1].style.display = "none";
            emailForm.children[0].children[1*2+1].children[1].classList.remove("flexible");
        }
    });
    emailInput.addEventListener("input", function(event) {
        if (helpTextArr[2].style.display === "block") {
            emailInput.parentNode.classList.remove("invalid");
            helpTextArr[2].style.display = "none";
            emailForm.children[0].children[2*2+1].children[1].classList.remove("flexible");
        }
    });
    document.getElementById("send-email").addEventListener("click", function(e) {
        for (let i = 0; i < 2; i++){
            if(emailForm[i].checkValidity() && (! emailForm[i].validity["valueMissing"] || ! emailForm[i].validity["patternMismatch"] )) {
                validIndicator(emailForm, i);
            } else {
                errorIndicator(emailForm, i);
            }
        }
        if(validateEmail(emailForm[2].value) === false){
            e.preventDefault();
            errorIndicator(emailForm, 2);
        } else {
            validIndicator(emailForm, 2);
        }
    });

    $(".thumbnail img").click(function(event) {
        for(let i = 0; i < 12; i++){
            if (this.parentNode === $(".stars-container")[0].children[i]) {
                lightBox.imageIndex = i+1;
            }
        }
        document.getElementById("lightbox").style.display = "flex";
        document.getElementById("lightbox").getElementsByTagName("img")[0].attributes[0].value = this.attributes[0].value;
    });

    $(".lightbox .close").click(function(event) {
        document.getElementById("lightbox").style.display = "none";
    });

    $(".lightbox .prev").click(function(event) {
        carousel.minusIndex(lightBox, 1);
        lightBox.changeImg();
    });

    $(".lightbox .next").click(function(event) {
        carousel.plusIndex(lightBox, 1);
        lightBox.changeImg();
    });

    $(".person-card-nav .prev").click(function(event) {
        carousel.minusIndex(slideShow, 1);
        slideShow.changeSlide();
    });

    $(".person-card-nav .next").click(function(event) {
        carousel.plusIndex(slideShow, 1);
        slideShow.changeSlide();
    });
    
    $(".person-card").click(function(event) {
        
    });
});