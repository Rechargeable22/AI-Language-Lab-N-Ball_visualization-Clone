col1 = document.getElementById("col1");
col2 = document.getElementById("col2");
col3 = document.getElementById("col3");

// let dataDict = {
//     ["ThemaA"]: ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"],
//     ["ThemaB"]: ["B1", "B2", "B3", "B4"],
//     ["ThemaC"]: ["C1", "C2", "C3", "C4"]
// };

function clearFirstCol() {
    let child = col1.lastElementChild;
    while (child) {
        col1.removeChild(child);
        child = col1.lastElementChild;
    }

}

function clearSecondCol() {
    let child = col2.lastElementChild;
    while (child) {
        col2.removeChild(child);
        child = col2.lastElementChild;
    }
    for (var c = col1.firstChild; c !== null; c = c.nextSibling) {
        c.classList.remove("active")
    }
}

function clearThirdCol() {
    let child = col3.lastElementChild;
    while (child) {
        col3.removeChild(child);
        child = col3.lastElementChild;
    }
    for (var c = col2.firstChild; c !== null; c = c.nextSibling) {
        c.classList.remove("active")
    }
}

function createTextDiv(t) {
    const divNode = document.createElement("a");
    const text = document.createTextNode(t);
    divNode.className = "list-group-item list-group-item-action";
    divNode.appendChild(text);
    divNode.classList.add("clickable");
    return divNode;
}

function buildFolders(dataDict) {
    col1 = document.getElementById("col1");
    col2 = document.getElementById("col2");
    col3 = document.getElementById("col3");

    for (const key in dataDict.input_words) {
        const divNode = createTextDiv(dataDict.input_words[key]);
        divNode.addEventListener("click", function () {
            clearSecondCol();
            clearThirdCol();
            divNode.classList.add("active");

            const elementsToAdd = dataDict.word_senses[dataDict.input_words[key]];

            for (const [index, element] of elementsToAdd.entries()) {
                const textElement = createTextDiv(element);
                textElement.addEventListener("click", function () {
                    clearThirdCol();
                    textElement.classList.add("active");
                    const definition = createTextDiv(dataDict.word_definitions[dataDict.input_words[key]][index]);
                    col3.appendChild(definition);
                });
                col2.appendChild(textElement)
            }

        });
        col1.appendChild(divNode);
    }
}

window.onload = function () {
    let submitForm = document.getElementById("input-words");
    submitForm.addEventListener('submit', postName);

    function postName(e) {
        e.preventDefault();

        var name = document.getElementById('input-text-field').value;
        var params = "name=" + name;

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/', true);
        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

        xhr.onload = function () {

            let dataDict = JSON.parse(this.responseText);
            buildFolders(dataDict);
        };

        xhr.send(params);
        clearThirdCol();
        clearSecondCol();
        clearFirstCol();

    }
};