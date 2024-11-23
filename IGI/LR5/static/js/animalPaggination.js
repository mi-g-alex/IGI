class AnimalPaggination {

    #contatiner

    #animals = []
    #currentPage = 1
    #pagginationDiv

    constructor(animalList, div) {
        this.#contatiner = div
        this.#animals = animalList
        this.buildAnimalView()
    }

    buildAnimalView() {
        let end = this.#currentPage * 3;
        if (end > this.#animals.length) end = this.#animals.length;
        this.#contatiner.innerHTML = "";
        let gC = document.createElement("div")
        gC.className = "grid-container"

        for (let i = (this.#currentPage - 1) * 3; i < end; i++) {
            let elem = document.createElement('div')
            elem.className = "animal-element"
            let cont = document.createElement('div')
            cont.className = "animal-container"


            let img = document.createElement('img')
            img.src = this.#animals[i].url

            let infoDiv = document.createElement('div')
            infoDiv.className = "animal-details"
            infoDiv.style.setProperty('transform: ', 'scew(10deg, 10deg')

            let name = document.createElement('h2')
            name.textContent = this.#animals[i].name

            let family = document.createElement('p')
            family.innerHTML = "Family: " + this.#animals[i].family

            let countries = document.createElement('p')
            countries.innerHTML = "Countries: " + this.#animals[i].countries

            let facts = document.createElement('p')
            facts.innerHTML = "Facts: " + this.#animals[i].facts

            infoDiv.appendChild(name)
            infoDiv.appendChild(family)
            infoDiv.appendChild(countries)
            infoDiv.appendChild(facts)

            elem.addEventListener('mousemove', function (e) {
                const [x, y] = [e.offsetX, e.offsetY];
                const rect = elem.getBoundingClientRect();
                const [width, height] = [rect.width, rect.height];
                const middleX = width / 2;
                const middleY = height / 2;
                const offsetX = ((x - middleX) / middleX) * 25;
                const offsetY = ((y - middleY) / middleY) * 25;
                cont.style.setProperty("--rotateX", 1 * offsetX + "deg");
                cont.style.setProperty("--rotateY", -1 * offsetY + "deg");
            });

            cont.addEventListener('mouseleave', function () {
                cont.style.setProperty("--rotateX", 0 + "deg");
                cont.style.setProperty("--rotateY", 0 + "deg");
            });

            cont.appendChild(img)
            cont.appendChild(infoDiv)

            elem.appendChild(cont)

            gC.appendChild(elem)
        }

        this.#pagginationDiv = document.createElement('div')
        this.#pagginationDiv.style.marginTop = "10px"
        this.#contatiner.appendChild(gC);
        this.#contatiner.appendChild(this.#pagginationDiv)
        this.updatePaggination()
    }

    updatePaggination() {
        this.#pagginationDiv.innerHTML = "";
        for (let i = 0; i < Math.ceil(this.#animals.length / 3); i++) {
            var nmb = document.createElement('a')
            nmb.addEventListener('click', () => {
                this.#currentPage = i + 1;
                this.buildAnimalView()
            }
            )
            nmb.innerHTML = i + 1;
            nmb.style.marginRight = "10px"
            if (this.#currentPage == i + 1) {
                nmb.style.textDecoration = "underline"
                nmb.style.color = "#f00"
            }
            this.#pagginationDiv.appendChild(nmb)
        }
    }

}