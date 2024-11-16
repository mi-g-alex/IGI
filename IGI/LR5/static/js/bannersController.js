class BannerController {

    listOfItems = [] // Список элементов
    itemsCount = 0  // Количество элеметов в списке
    isLoop = true // Настройка цикличности
    showNavs = true // Настройка показывать ли стрелочки
    usePagination = true // Натсрйока Показывать точечки снизу  
    autoSwitchTimerId
    delay = 5000 // Время автосвапа в ms
    autoSwitch = true // Включен ли авттосвап
    stopOnMouseHover = true // Настройка остановки при наведении мыши

    currentSlide = 0
    
    pagginControlsButtonsDiv
    pagginButtons = [];
    currentStateText
    nextSlideButton 
    prevSlideButton
    
    slideImage
    slideTitle

    constructor(listOfItems, div) {
        const slider = document.createElement('div')
        slider.className = 'slider'
        
        const contorls = document.createElement('div')
        contorls.className = 'controls'
        
        const paggingControls = document.createElement('div')
        paggingControls.className = 'paggin-cotrols'

        const currentText = document.createElement('p')
        currentText.className = 'current-page-text'

        const prevButton = document.createElement('button');
        prevButton.className = 'button-prev';
        prevButton.addEventListener('click', () => { this.goPrev() })
        
        const nextButton = document.createElement('button');
        nextButton.className = 'button-next';
        nextButton.addEventListener('click', () => { this.goNext() })

        contorls.appendChild(paggingControls)
        slider.appendChild(currentText)
        contorls.appendChild(prevButton)
        contorls.appendChild(nextButton)

        const slides = document.createElement('div')
        slides.className = 'slides'

        const slideImg = document.createElement('img')
        slideImg.className = 'slide-img'
        slideImg.addEventListener('mouseover', () => { this.stopAutoSwith() })
        slideImg.addEventListener('mouseout', () => { this.startAutoSwith() })
        
        const slideTitle = document.createElement('h2')
        slideTitle.className = 'slide-label'
        
        slides.appendChild(slideImg)
        slides.appendChild(slideTitle)

        slider.appendChild(contorls)
        slider.appendChild(slides)
        
        div.appendChild(slider)

        this.listOfItems = listOfItems;
        this.itemsCount = listOfItems.length;
        this.pagginControlsButtonsDiv = paggingControls;
        this.currentStateText = currentText
        this.nextSlideButton = nextButton
        this.prevSlideButton = prevButton
        this.slideImage = slideImg
        this.slideTitle = slideTitle

        this.setupBanner()
    }

    set setLoop(enabled) {
        this.isLoop = Boolean(enabled)
        this.setItemById(this.currentSlide)
    }

    set setNavs(enabled) {
        this.showNavs = Boolean(enabled)
        this.nextSlideButton.style.visibility = this.showNavs ? 'visible' : 'hidden';
        this.prevSlideButton.style.visibility = this.showNavs ? 'visible' : 'hidden';
    }

    set setPagination(enabled) {
        this.usePagination = Boolean(enabled)
        console.log("set pag " + enabled)
        this.pagginControlsButtonsDiv.style.display = enabled ? 'visible' : 'none';
    }
    
    set setDelay(newDelay) {
        if(Number(newDelay) < 500) {
            console.log("Little delay")
            return;
        }
        this.delay = Number(newDelay)
        this.stopAutoSwith()
        this.startAutoSwith()
    }
    
    set setAutoSwitch(enabled) {
        this.autoSwitch = Boolean(enabled)
        if(!enabled) 
            this.stopAutoSwith()
        else 
            this.startAutoSwith()
    }
    
    set setStopOnMouseHover(enabled) {
        this.stopOnMouseHover = Boolean(enabled)
    }

    setupBanner() {
        for (let i = 0; i < this.itemsCount; i++) {
            const button = document.createElement('button');
            button.className = 'button-pagging-control';
            const clickHandler = () => this.setItemById(i);
            button.addEventListener('click', clickHandler)
            this.pagginControlsButtonsDiv.appendChild(button);
            this.pagginButtons.push(button);
        }
        this.currentSlide = 0;
        this.setItemById(0);
        this.startAutoSwith()
    }

    setItemById(id) {
        this.changeSelectedDot(this.currentSlide, id)
        this.currentSlide = Number(id)
        this.slideImage.src = this.listOfItems[id].imageSrc;
        this.slideImage.onclick = () => {window.open(this.listOfItems[id].url)}
        this.slideTitle.textContent = this.listOfItems[id].title;
        this.currentStateText.innerHTML = "" + String(id + 1) + "/" + this.itemsCount

        if(this.showNavs && !this.isLoop) {
            this.nextSlideButton.style.visibility = this.currentSlide == this.itemsCount - 1 ? 'hidden' : 'visible'
            this.prevSlideButton.style.visibility = this.currentSlide == 0 ? 'hidden' : 'visible'
        }
    }

    goNext() {
        console.log("Go next image")
        if(this.isLoop == false && this.currentSlide == this.itemsCount - 1) return;
        this.setItemById(this.currentSlide == this.itemsCount - 1 ? 0 : this.currentSlide + 1)
    }

    goPrev() {
        if(!this.isLoop && this.currentSlide == 0) return;
        console.log("Go prev image")
        this.setItemById(this.currentSlide == 0 ? this.itemsCount - 1 : this.currentSlide - 1)
    }

    changeSelectedDot(prevN, nextN) {
        let prevBtn = this.pagginButtons[prevN]
        let nextBtn = this.pagginButtons[nextN]
        prevBtn.className = 'button-pagging-control'
        nextBtn.className = 'button-pagging-control active'
    }

    startAutoSwith() {
        console.log("Start auto switch")
        if(this.autoSwitch) {
            let f = () => { this.goNext() }
            this.autoSwitchTimerId = setInterval(f, this.delay)
            console.log(this.autoSwitchTimerId)
        }
    }

    stopAutoSwith() {
        if(this.stopOnMouseHover) {
            console.log("Stop auto switch")
            clearInterval(this.autoSwitchTimerId)
            this.autoSwitchTimerId = null
        }
    }
    
}