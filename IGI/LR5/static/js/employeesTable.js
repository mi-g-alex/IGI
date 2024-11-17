class EmployeeTable {

    #tableDiv
    #dataDiv
    #preloader
    #inputDiv
    #inputField = ""
    #columntHeaders = ["", "Photo", "Name", "Phone number", "Email", "About"]
    #sortField
    #data = []
    #table
    #selectedEmplyees = []

    #currentPage = 1;
    #pagginationDiv

    #generateButton

    constructor(data, div, dataDiv) {
        this.#dataDiv = dataDiv
        this.#preloader = div.querySelector('.preloader')
        div.removeChild(this.#preloader)
        this.#tableDiv = document.createElement('div')
        this.#inputDiv = document.createElement('div')
        this.#generateButton = document.createElement('button')
        this.#generateButton.textContent = 'Премировать';
        this.#generateButton.style.visibility = 'hidden'
        this.#generateButton.style.marginTop = '10px';
        this.#generateButton.addEventListener('click', () => {
            this.generatePrem()
        })

        this.#inputDiv.style.marginBottom = "10px"
        this.#pagginationDiv = document.createElement('div')
        this.#pagginationDiv.style.marginTop = "10px"
        this.#buildTextField()

        
        const addButton = document.createElement('button');
        addButton.id = 'add-button';
        addButton.textContent = 'Add new';
        addButton.style.marginBottom = "10px"

        addButton.addEventListener('click', () => {
            window.open("add", "_self")
        });

        div.append(addButton)
        div.append(this.#inputDiv)
        div.append(this.#tableDiv)
        div.append(this.#pagginationDiv)
        div.append(this.#generateButton)
        this.#data = data
        this.#table = this.#buildTable()
        this.#tableDiv.appendChild(this.#table)
        this.loadData()
    }

    #buildTextField() {
        const input = document.createElement('input');
        input.type = 'text';
        input.id = 'search-input';

        const filterButton = document.createElement('button');
        filterButton.id = 'search-button';
        filterButton.textContent = 'Filter';

        filterButton.addEventListener('click', () => {
            const searchText = input.value;
            this.#inputField = searchText
            this.loadData()
        });

        this.#inputDiv.appendChild(input);
        this.#inputDiv.appendChild(filterButton);
    }


    #buildTable() {
        const table = document.createElement('table');
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');

        this.#columntHeaders.forEach(headerText => {
            const th = document.createElement('th');
            th.addEventListener('click', () => {
                this.#setSort(headerText)
            })
            let txt = headerText;
            if (this.#sortField != "" && this.#sortField != "-") {
                if (this.getSortTypeByFieldName(headerText) == this.#sortField) txt += "↥"
                if ("-" + this.getSortTypeByFieldName(headerText) == this.#sortField) txt += "↧"
            }
            th.textContent = txt;
            headerRow.appendChild(th);
        });

        thead.appendChild(headerRow);
        table.appendChild(thead);

        return table;
    }

    getSortTypeByFieldName(headerText) {
        switch (headerText) {
            case "Name":
                return "name";
            case "Phone number":
                return "phone";
            case "Email":
                return "email";
            case "About":
                return "info";
            default:
                return "";
        }
    }

    #setSort(headerText) {

        let check = (inp) => {
            if (this.#sortField != inp && this.#sortField != "-" + inp) {
                this.#sortField = inp
            } else {
                this.#sortField = (this.#sortField == inp ? "-" : "") + inp
            }
        }

        check(this.getSortTypeByFieldName(headerText))

        this.loadData()
    }

    async loadData() {
        this.#tableDiv.removeChild(this.#table)
        this.#tableDiv.appendChild(this.#preloader)
        setTimeout(async () => {
            this.#currentPage = 1;
            this.#selectedEmplyees = [];
            const url = new URL('http://localhost:8000/super/employees/filter');
            const params = {
                filter: this.#inputField,
                sort: this.#sortField
            };

            Object.keys(params).forEach(key => {
                if (params[key]) {
                    url.searchParams.append(key, params[key]);
                }
            });

            const response = await fetch(url);
            const data = await response.json();
            this.#data = data;
            this.#pagginationDiv.innerHTML = "";
            this.#tableDiv.appendChild(this.#table)
            this.#tableDiv.removeChild(this.#preloader)
            this.updateRows()
            this.#preloader.style.dysplay = 'none'
        }, 1000
        )
    }

    onRowClick(employee) {
        this.#dataDiv.innerHTML = ""

        const card = document.createElement('div');
        card.className = 'employee-card';

        const photoDiv = document.createElement('div');
        photoDiv.className = 'employee-photo';
        const img = document.createElement('img');
        img.src = "/" + employee.photo;
        photoDiv.appendChild(img);

        const infoDiv = document.createElement('div');
        infoDiv.className = 'employee-info';

        const nameElement = document.createElement('h3');
        nameElement.textContent = employee.name;

        const phoneElement = document.createElement('p');
        phoneElement.innerHTML = `<strong>PN.:</strong> ${employee.phone}`;

        const emailElement = document.createElement('p');
        emailElement.innerHTML = `<strong>Email:</strong> ${employee.email}`;

        const infoElement = document.createElement('p');
        infoElement.innerHTML = `<strong>Info:</strong> ${employee.info}`;

        infoDiv.appendChild(nameElement);
        infoDiv.appendChild(phoneElement);
        infoDiv.appendChild(emailElement);
        infoDiv.appendChild(infoElement);

        card.appendChild(photoDiv);
        card.appendChild(infoDiv);

        this.#dataDiv.appendChild(card);
    }

    #onSelectedChagne() {
        if (this.#selectedEmplyees.length > 0) {
            this.#generateButton.style.visibility = 'visible'
        } else {
            this.#generateButton.style.visibility = 'hidden'
        }
    }

    generatePrem() {
        let text = "Премировать"
        this.#selectedEmplyees.forEach(empl => {
            text += " " + empl.fields.name + ", "
        })
        this.#dataDiv.innerHTML = ""
        const txt = document.createElement('h3');
        txt.textContent = text

        this.#dataDiv.appendChild(txt);

    }

    updateRows() {
        this.#tableDiv.removeChild(this.#table)
        this.#table = this.#buildTable()
        const tbody = document.createElement('tbody');

        let end = this.#currentPage * 3
        if (end >= this.#data.length) end = this.#data.length

        for (let i = (this.#currentPage - 1) * 3; i < end; i++) {
            console.log(i);
            const employee = this.#data[i];
            console.log(employee.fields);
            const row = document.createElement('tr');
            row.addEventListener('click', () => {
                this.onRowClick(employee.fields)
            })

            const checkboxCell = document.createElement('td');
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.addEventListener('change', () => {
                if (checkbox.checked) {
                    this.#selectedEmplyees.push(employee)
                } else {
                    const index = this.#selectedEmplyees.indexOf(employee);
                    if (index > -1) {
                        this.#selectedEmplyees.splice(index, 1);
                    }
                }
                this.#onSelectedChagne()
            })
            checkboxCell.appendChild(checkbox);
            row.appendChild(checkboxCell);

            const photoCell = document.createElement('td');
            const imgDiv = document.createElement('div')
            imgDiv.className = "employee-photo"
            const img = document.createElement('img');
            img.src = "/" + employee.fields.photo;
            imgDiv.appendChild(img)
            photoCell.appendChild(imgDiv);
            row.appendChild(photoCell);

            const nameCell = document.createElement('td');
            nameCell.textContent = employee.fields.name;
            row.appendChild(nameCell);

            const phoneCell = document.createElement('td');
            phoneCell.textContent = employee.fields.phone;
            row.appendChild(phoneCell);

            const emailCell = document.createElement('td');
            emailCell.textContent = employee.fields.email;
            row.appendChild(emailCell);

            const descriptionCell = document.createElement('td');
            descriptionCell.textContent = employee.fields.info;
            row.appendChild(descriptionCell);

            tbody.appendChild(row);
        };

        this.#table.appendChild(tbody);
        this.#tableDiv.appendChild(this.#table)

        this.updatePaggination()
    }

    updatePaggination() {
        this.#pagginationDiv.innerHTML = "";
        for (let i = 0; i < Math.ceil(this.#data.length / 3); i++) {
            var nmb = document.createElement('a')
            nmb.addEventListener('click', () => {
                this.#currentPage = i + 1;
                this.updateRows()
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